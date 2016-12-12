import svn_utils
import svn.remote
import urllib2
from getpass import getpass
import requests
import os.path
from dateutil import parser as date_parser

FORCE_UPDATE = False # when True no time stamp are checked and updates are performed

REMOTE_REPO_URL = 'http://svn.code.sf.net/p/tango-ds/code'
LOCAL_REPO_URL = 'file:///home/piotr/tmp/test-svn/'
REPO_START_PATH = 'DeviceClasses/Vacuum'

SERVER_BASE_URL = 'http://localhost:8080'

SERVER_DSC_URL = SERVER_BASE_URL+'/resources/dsc/'

SERVER_ADD_URL = SERVER_BASE_URL+'/resources/dsc/add/'

SERVER_LIST_URL = SERVER_BASE_URL+'/resources/dsc/list/?repository_url='

SERVER_LOGIN_URL = SERVER_BASE_URL+'/account/sign-in/?next=/resources/dsc/'

LOG_PATH = '/home/piotr/tmp'

print "You are going to update a devcie servers catalogue info on the server: %s" % SERVER_BASE_URL

login = raw_input('Login:')
password = getpass()

client = requests.session()

client.get(SERVER_LOGIN_URL)  # sets the cookie
csrftoken = client.cookies['csrftoken']
print csrftoken

login_data = dict(login=login, password=password, csrfmiddlewaretoken=csrftoken)
r = client.post(SERVER_LOGIN_URL, data=login_data)

if r.status_code!=200:
    print "wrong password or sever connection error."
    exit()
else:
    print 'Successfully logged in to catalogue server.'

print 'Getting a list of device server in the repository...'


repo = svn.remote.RemoteClient(LOCAL_REPO_URL)
ds_list = svn_utils.get_device_servers_list(repo,REPO_START_PATH,10)

ds_problems = []

print 'Found %d device servers.' % len(ds_list)

for ds in ds_list:
    print
    print '------------------------------------'
    print 'Processing %s' % ds['path']

    if len(ds['xmi_files'])==0:
        print 'No .xmi files found in this path. Skipping.'
        continue

    print 'Check if device server already exists in the catalogue...'

    r = client.get(SERVER_LIST_URL+REMOTE_REPO_URL+'/'+ds['path'])
    ds_on_server = r.json()
    print "Devcie servers in the catalogu: "
    print  ds_on_server
    if len(ds_on_server)>1:
        print 'There are %d device servers registered with this repository path. ' \
              'Import utility does not handle such case. Skipping.  '
        continue

    files = {}

    if len(ds_on_server)==1:
        print 'This device server already exists in catalogue. Will do update if necessary.'
        server_ds_pk, server_ds = ds_on_server.popitem()
    else:
        print 'This is a new device server. Will add to catalogue.'

    ds_repo_url = REMOTE_REPO_URL + '/' + ds['path']

    # readme file
    upload_readme = 0
    if len(ds['readme_files'])>0:
        readme_file = ds['readme_files'][0]
        readme_name = readme_file['name']
        print 'There is a readme file: %s' % readme_name
        if os.path.splitpath(readme_name)[1] not in ['.txt', '.TXT',
                                                     '.md', '.MD',
                                                     '', '.doc', '.DOC',
                                                     '.rst', '.RST',
                                                     '.pdf', '.PDF',
                                                     '.html', '.HTML', '.htm', '.HTM']:
            print 'Will skip file of unknown extension.'
        else:
            if len(ds_on_server) == 0 or FORCE_UPDATE or \
                    date_parser.parse(ds_on_server[0]['last_update']) < date_parser.parse(readme_file['element']['date']):
                # get file from the server
                readme_url_response = urllib2.urlopen(REMOTE_REPO_URL+'/'+readme_file['path'])
                readme_file_size = int(readme_url_response.info().get('Content-Length',0))
                if readme_file_size < 5 or readme_file_size > 2000000:
                    print 'Readme file sieze %d is out of limits. Skipping.' % readme_file_size
                else:
                    print 'It will be uploaded.'
                    read_file_content=readme_url_response.read()
                    files = {'readme': (readme_name, read_file_content)}
                    upload_readme = 1
            else:
                print 'Will skip the readme upload since it is elder than the last update of device server.'


    # xmis
    first_xmi=True
    for xmi in ds['xmi_files']:
        print "XMI file: %s" % xmi['name']
        xmi_url = REMOTE_REPO_URL + '/' + xmi['path']

        if first_xmi:
            if len(ds_on_server)==0:
                client.get(SERVER_ADD_URL)  # sets the cookie
                csrftoken = client.cookies['csrftoken']
                r = client.post(SERVER_ADD_URL,
                            data={
                                'csrfmiddlewaretoken': csrftoken,
                                'xmi_file_url':xmi_url,
                                'use_url_xmi_file': 1,
                                'use_manual_info': False,
                                'use_uploaded_xmi_file': False,
                                'repository_url': ds_repo_url,
                                'repository_type': 'SVN',
                                'upload_readme': upload_readme,
                                'submit': 'create',
                                'platform': 'Windows',
                                'language': 'CPP'

                            },
                            files=files)
                print r

                with open(LOG_PATH+'/add.html', 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=128):
                        fd.write(chunk)

                first_xmi = False

                r = client.get(SERVER_LIST_URL + REMOTE_REPO_URL + '/' + ds['path'])
                ds_on_server = r.json()
                if len(ds_on_server) == 1:
                    print 'This device server already exists in catalogue. Will do update if necessary.'
                    server_ds_pk, server_ds = ds_on_server.popitem()
                else:
                    print 'It seems the device server has not been add to the catalogue...'
                    ds_problems.append(ds)
                    continue
            else:
                client.get(SERVER_DSC_URL+'/ds/'+str(server_ds_pk)+'/update')  # sets the cookie
                csrftoken = client.cookies['csrftoken']
                client.post(SERVER_DSC_URL+'/ds/'+str(server_ds_pk)+'/update',
                            data={
                                'csrfmiddlewaretoken': csrftoken,
                                'add_class': False,
                                'xmi_file_url':xmi_url,
                                'use_url_xmi_file': 1,
                                'use_manual_info': False,
                                'use_uploaded_xmi_file': False,
                                'repository_url': ds_repo_url,
                                'repository_type': 'SVN',
                                'upload_readme': upload_readme,
                                'submit': 'update'
                            },
                            files=files)
                first_xmi = False

        else:
            client.get(SERVER_DSC_URL + '/ds/' + str(server_ds_pk) + '/update')  # sets the cookie
            csrftoken = client.cookies['csrftoken']
            client.post(SERVER_DSC_URL+'/ds/'+str(server_ds_pk)+'/update',
                        data={
                            'csrfmiddlewaretoken': csrftoken,
                            'add_class': 1,
                            'xmi_file_url':xmi_url,
                                'use_url_xmi_file': 1,
                                'use_manual_info': False,
                                'use_uploaded_xmi_file': False,
                                'repository_url': ds_repo_url,
                                'repository_type': 'SVN',
                                'upload_readme': upload_readme,
                                'submit': 'update'
                        })








