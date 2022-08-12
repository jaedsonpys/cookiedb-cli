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
        self._databases_dir_path = os.path.join(self._home_user, '.cookiedb')

        self._cookiedb: cookiedb.CookieDB = None

    def get_database(self) -> list:
        if not os.path.isdir(self._database_dir_path):
            os.mkdir(self._databases_dir_path)
            databases = []
        else:
            listdir = os.listdir(self._database_dir_path)
            databases = [db for db in listdir if db.endswith('.cookiedb')]

        return databases

    def initial_config(self, password: str) -> bytes:
        pw_hash = hashlib.md5(password)
        b64_hash = base64.urlsafe_b64encode(pw_hash)

        password_file = os.path.join(self._databases_dir_path, '.user')

        with open(password_file, 'wb') as writer:
            writer.write(b64_hash)

        self._cookiedb = cookiedb.CookieDB(
            key=b64_hash,
            database_local=self._databases_dir_path
        )

        return b64_hash
