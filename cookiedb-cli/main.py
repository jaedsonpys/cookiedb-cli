import os
import getpass
import readline
import base64
import hashlib
import pathlib

import cookiedb
from cryptography import fernet


class CookieDBCLI(object):
    def __init__(self):
        self._home_user = pathlib.Path.home()
        self._database_dir_path = os.path.join(self._home_user, '.cookiedb')

    def get_database(self) -> list:
        if not os.path.isdir(self._database_dir_path):
            os.mkdir(self._database_dir_path)
            database = []
        else:
            listdir = os.listdir(self._database_dir_path)
            database = [db for db in listdir if db.endswith('.cookiedb')]

        return database
