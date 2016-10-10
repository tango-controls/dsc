# -*- coding: utf-8 -*-
from git import Repo

class RepoHandler:
    """Base class for handling repositories """

    def __init__(self, temp_repo_path, xmi_storage_path, archives_storage_path):
        self.temp_repo_path = temp_repo_path
        self.xmi_sotrage_path = xmi_storage_path
        self.archives_storage_path = archives_storage_path
        self.connected = False
        self.downloaded = False


    def connect(self, url, path_within_repository):
        """
        Connects to repository. Creates internal information about it
        :param url:
        :param path_within_repository:
        :return:
        """
        pass

    def find_xmi(self):
        """
        Search the repository for xmi files
        :return: list of xmi files within repository
        """
        # TODO: implement find_xmi
        pass

    def archive_zip(self):
        """
        Return zip package of repository.
        :return: zipped repository
        """
        pass

    def archive_tar(self):
        """
        Return zip package of repository.
        :return: zipped repository
        """

        pass

    def get_session_data(self):
        """
        Provides information required to be persistent in a session
        :return: a dictionary containing data
        """

        # TODO: implement common part of get_session_data
        pass

    def revert_from_session_data(self, session_data):
        """
        Revert state of the handler basing on information from the session
        :param session_data: data from session
        :return:
        """

        # TODO: implement common part of reverting the handler from session data
        pass


class GitHandler(RepoHandler):
    """Class for handling Git repositories"""

    def __init__(self, temp_repo_path, xmi_storage_path, archives_storage_path):
        super(GitHandler,self).__init__(temp_repo_path, xmi_storage_path, archives_storage_path)

        # TODO: implement constructor

    def connect(self,url, path_within_repository):
        """
        Connects to repository. Creates internal information about it
        :param url:
        :param path_within_repository:
        :return:
        """
        # TODO: implement connect
        pass

    def checkout(self, branch, tag):
        """
        return the temporary generated sub_path (random_generated_name) and store it in self.download_path
        :param branch:
        :param tag:
        :return: a temporary generated sub_path (random_generated_name)
        """
        # TODO: implement checkout
        pass

    def find_xmi(self):
        """
        Search the repository for xmi files
        :return: list of xmi files within repository
        """
        # TODO: implement find_xmi
        pass

    def archive_zip(self):
        """
        Return zip package of repository.
        :return: zipped repository
        """
        # TODO: implement archive_zip
        pass

    def archive_tar(self):
        """
        Return zip package of repository.
        :return: zipped repository
        """
        # TODO: implement archive_zip
        pass

    def get_session_data(self):
        """
        Provides information required to be persistent within a session
        :return: a dictionary with data ready to be stored in session object
        """
        session_data = super(GitHandler, self).get_session_data()

        # TODO: implement GIT part of get_session_data
        pass

    def revert_from_session_data(self, session_data):
        """
        Revert state of the handler basing on information from the session
        :param session_data: data from session
        :return:
        """

        # TODO: implement GIT part of reverting the handler from session data
        pass


class SvnHandler(RepoHandler):
    pass