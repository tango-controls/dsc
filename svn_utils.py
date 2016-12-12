import svn.remote
import os.path
import datetime

def find_xmi(repo, path_base, max_depth):
    if max_depth<1:
        return []
    xmi_list = []
    try:
        objects_list = repo.list(extended=True, rel_path=path_base)

        for element in objects_list:
            # if it is a directory
            if element['is_directory']:
                xmi_list.extend(
                    find_xmi(repo=repo,
                             path_base=path_base + '/' + element['name'],
                             max_depth=max_depth - 1)
                )

            elif element['kind'] == 'file':

                # add just local files
                if os.path.splitext(element['name'])[1]=='.XMI' or os.path.splitext(element['name'])[1]=='.xmi':
                    print "File: %s" % element['name']
                    xmi_list.append({'name': element['name'],
                                            'path': path_base,
                                            'element': element
                                            })
    except:
        pass
    return xmi_list


def find_readme(repo, path_base, max_depth):
    if max_depth<1:
        return []
    readme_list = []
    try:
        objects_list = repo.list(extended=True, rel_path=path_base)

        for element in objects_list:
            # if it is a directory
            if element['is_directory']:
                readme_list.extend(
                    find_readme(repo=repo,
                             path_base=path_base + '/' + element['name'],
                             max_depth=max_depth - 1)
                )

            elif element['kind'] == 'file':

                # add just local files
                if os.path.splitext(element['name'])[0] in ['Readme', 'README']:
                    print "File: %s" % element['name']
                    readme_list.append({'name': element['name'],
                                            'path': path_base,
                                            'element': element
                                            })
    except:
        pass
    return readme_list


def get_device_servers_list(repo, path_base, max_depth):
    """"""
    if max_depth<1:
        return []

    print '----------------------'
    print "In %s " % path_base

    ds_list = []

    try:
        objects_list = repo.list(extended=True, rel_path=path_base)

        tag_xmi_files = []
        tag_readme_files = []
        trunk_xmi_files = []
        trunk_readme_files = []
        src_xmi_files = []
        src_readme_files = []
        local_xmi_files = []
        local_readme_files = []
        candidate_for_ds = False
        # iterate through the list
        for element in objects_list:

            if element is None:
                continue
            # if it is a directory
            if element['is_directory']:

                if element['name'] in ['tags','trunk', 'src']:
                    candidate_for_ds = True
                    print 'Path %s is a candidate.' % path_base

                if element['name']=='tags':
                    # for tags directory it is looking for the newest one:
                    newest_tag = None
                    newest_date = datetime.datetime.now()
                    try:
                        print '----------------------'
                        print 'Available tags:'
                        for t in repo.list(extended=True, rel_path=path_base+'/tags'):
                            try:
                                print '%s' % t['name']
                                if t['is_directory'] and (newest_tag is None or t['date']>newest_date):
                                    newest_tag = t['name']
                                    newest_date = t['date']
                            except Exception as e:
                                print 'Exception message: %s' %e.message
                    except Exception as e:
                        print 'Exception message: %s' %e.message


                    if newest_tag is None:
                        # there ara none sub-folders so let's assume this is the tag
                        newest_tag = ''

                    # get xmi files in the tag
                    tag_xmi_files = find_xmi(repo=repo, path_base=path_base+'/tags/'+newest_tag, max_depth=max_depth-1)
                    tag_readme_files = find_readme(repo=repo, path_base=path_base + '/tags/' + newest_tag,
                                             max_depth=max_depth - 1)
                    print 'Xmi files in tag %s:' % len(newest_tag)


                elif element['name']=='trunk':
                    trunk_xmi_files = find_xmi(repo=repo, path_base=path_base+'/trunk', max_depth=max_depth-1)
                    trunk_readme_files = find_readme(repo=repo, path_base=path_base + '/trunk', max_depth=max_depth - 1)

                elif element['name']=='src':
                    src_xmi_files = find_xmi(repo=repo, path_base=path_base+'/trunk', max_depth=max_depth-1)
                    src_readme_files = find_readme(repo=repo, path_base=path_base + '/trunk', max_depth=max_depth - 1)


                elif element['name']!='branches':
                    # we are not in device server base so just look recursively:
                    ds_list.extend(
                        get_device_servers_list(repo=repo,
                                                path_base=path_base+'/'+element['name'],
                                                max_depth=max_depth-1))

            elif element['kind']=='file' :

                # add just local files
                if os.path.splitext(element['name'])[1]=='.XMI' or os.path.splitext(element['name'])[1]=='.xmi':
                    print "File: %s" % element['name']
                    local_xmi_files.append({'name':element['name'],
                                            'path':path_base,
                                            'element':element
                                            })

                if os.path.splitext(element['name'])[0] in ['Readme', 'README']:
                    print "File: %s" % element['name']
                    local_readme_files.append({'name': element['name'],
                                            'path': path_base,
                                            'element': element
                                            })

        # check if we are a device server
        if len(tag_xmi_files)>0:
            ds_list.append({'path':path_base,
                            'xmi_files':tag_xmi_files,
                            'tag':newest_tag,
                            'readme_files':tag_readme_files
                            })

        elif len(trunk_xmi_files)>0:
            ds_list.append({'path': path_base,
                            'xmi_files': trunk_xmi_files,
                            'readme_files':trunk_readme_files
                            })

        elif len(src_xmi_files)>0:
            ds_list.append({'path': path_base,
                            'xmi_files': src_xmi_files,
                            'readme_files': src_readme_files
                            })

        elif len(local_xmi_files)>0:
            ds_list.append( {'path': path_base,
                            'xmi_files': local_xmi_files,
                             'readme_files': local_readme_files
                            } )

        elif candidate_for_ds:
            ds_list.append({'path':path_base, 'xmi_files':[] })
    except Exception as e:
        print 'Exception message outer: %s' %e.message
        # raise e

    return ds_list







