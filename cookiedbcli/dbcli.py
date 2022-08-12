import base64
import hashlib
import os
import pathlib
from typing import Union

import cookiedb

from . import exceptions


class CookieDBCLI(object):
    def __init__(self):
        self._home_user = pathlib.Path.home()
        self._databases_dir_path = os.path.join(self._home_user, '.cookiedb')

        self._cookiedb: cookiedb.CookieDB = None

    def get_databases(self) -> list:
        if not os.path.isdir(self._database_dir_path):
            os.mkdir(self._databases_dir_path)
            databases = []
        else:
            listdir = os.listdir(self._database_dir_path)
            databases = [db for db in listdir if db.endswith('.cookiedb')]

        return databases

    def set_database_dir(self, path: str) -> None:
        if os.path.isdir(path):
            self._databases_dir_path = path
        else:
            raise FileNotFoundError(f'Directory "{path}" not found')

    def configure(self, password: str) -> bytes:
        if not os.path.isdir(self._database_dir_path):
            os.mkdir(self._databases_dir_path)

        password_file = os.path.join(self._databases_dir_path, '.user')

        if not os.path.isfile(password_file):
            pw_hash = hashlib.md5(password)
            b64_hash = base64.urlsafe_b64encode(pw_hash)

            with open(password_file, 'wb') as writer:
                writer.write(b64_hash)
        else:
            with open(password_file, 'r') as reader:
                b64_hash = reader.read()

        self._cookiedb = cookiedb.CookieDB(
            key=b64_hash,
            database_local=self._databases_dir_path
        )

        return b64_hash

    def _permitted_cmd(self, cmd_string: str) -> bool:
        db_methods = [
            'open', 'create_database', 'add',
            'get', 'delete', 'checkout'
        ]

        permitted = False

        if cmd_string.startswith('db.') and cmd_string[-1] == ')':
            if ';' not in cmd_string and '#' not in cmd_string:
                try:
                    db, method = cmd_string.split('.', maxsplit=1)
                except ValueError:
                    pass
                else:
                    open_backets_index = method.index('(')
                    method_name = method[0:open_backets_index]

                    if method_name in db_methods:
                        permitted = True

        return permitted

    def execute(self, command: str) -> Union[None, str]:
        command = command.strip()
        db = self._cookiedb
        result = None

        if self._permitted_cmd(command):
            exec(f'result = {command}')
        else:
            raise exceptions.InvalidCommandError(f'Command "{command}" unknown')

        return result
