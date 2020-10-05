from github3 import login
from github3.repos.contents import Contents
from models import DeviceServer, DeviceServerActivity, DscGitHubBackupConfig
from xmi_parser import TangoXmiParser


def save_xmi_on_github(ds, xmi, json_dictionary, request):
    """Saves backup of xmi file on the GitHub """

    try:
        github_config = DscGitHubBackupConfig.objects.latest('created_at')
        assert (isinstance(github_config, DscGitHubBackupConfig))
    except DscGitHubBackupConfig.DoesNotExist:
        # break here if there is no authentication provided
        return

    gh = login(token=github_config.oauth_token)

    repository = gh.repository(github_config.repository_owner, github_config.repository_name)

    default_family = None

    # if the xmi file is ok save claseses
    if repository is not None and xmi[1]:
        parser = TangoXmiParser(xml_string=xmi[0])

        # iterate through all classes in the xmi file
        for cl in parser.get_device_classes():
            directory = parser.get_device_class_info(cl).class_family
            # save default family for future
            if default_family is None or cl.name == ds.name:
                default_family = directory

            directory_contents = repository.contents(directory, github_config.branch)

            # save .xmi file
            file_name = str(ds.id) + '_' + cl.name + '.xmi'

            if directory_contents is not None and directory_contents.has_key(file_name):
                # if file already exists in the repository - update it
                xmi_contents = directory_contents[file_name]
                assert (isinstance(xmi_contents, Contents))

                xmi_contents.update(
                    message="Device class " + cl.name +" updated by " + request.user.get_full_name(),
                    content=xmi[0],
                    branch=github_config.branch,
                    committer={
                        "name": request.user.get_full_name(),
                        "email": request.user.email
                    }
                )
            else:
                repository.create_file(
                    path=directory+"/" + file_name,
                    message="Device class " + cl.name + " created by " + request.user.get_full_name(),
                    content=xmi[0],
                    branch=github_config.branch,
                    committer={
                                 "name": request.user.get_full_name(),
                                 "email": request.user.email
                              }
                )

            # save json file
            directory_contents = repository.contents(directory, github_config.branch)
            file_name = str(ds.id) + '_' + ds.name + '.json'

            if directory_contents is not None and directory_contents.has_key(file_name):
                # if file already exists in the repository - update it
                xmi_contents = directory_contents[file_name]
                assert (isinstance(xmi_contents, Contents))

                xmi_contents.update(
                    message="Device server " + ds.name + " updated by " + request.user.get_full_name(),
                    content=json_dictionary,
                    branch=github_config.branch,
                    committer={
                        "name": request.user.get_full_name(),
                        "email": request.user.email
                    }
                )
            else:
                repository.create_file(
                    path=directory + "/" + file_name,
                    message="Device server " + ds.name + " created by " + request.user.get_full_name(),
                    content=json_dictionary,
                    branch=github_config.branch,
                    committer={
                        "name": request.user.get_full_name(),
                        "email": request.user.email
                    }
                )