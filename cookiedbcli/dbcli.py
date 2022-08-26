# CookieDB CLI
# Copyright (C) 2022  Jaedson Silva
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import base64
import hashlib
import os
import pathlib
from typing import Union
from datetime import datetime

import cookiedb

from . import exceptions


class CookieDBCLI(object):
    def __init__(self):
        self._home_user = pathlib.Path.home()
        self._databases_dir_path = os.path.join(self._home_user, '.cookiedb')

        self._cookiedb: cookiedb.CookieDB = None

    def get_databases(self) -> list:
        if not os.path.isdir(self._databases_dir_path):
            os.mkdir(self._databases_dir_path)
            databases = []
        else:
            listdir = os.listdir(self._databases_dir_path)
            databases = [db for db in listdir if db.endswith('.cookiedb')]

        return databases

    def set_database_dir(self, path: str) -> None:
        if os.path.isdir(path):
            self._databases_dir_path = path
        else:
            raise FileNotFoundError(f'Directory "{path}" not found')

    def configure(self, password: str) -> None:
        pw_hash = hashlib.md5(password.encode()).hexdigest()
        b64_hash = base64.urlsafe_b64encode(pw_hash.encode())

        self._cookiedb = cookiedb.CookieDB(
            key=b64_hash,
            database_local=self._databases_dir_path
        )

    def create_info_database(self) -> None:
        self._cookiedb.create_database('cookiedbcli-info')
        self._cookiedb.open('cookiedbcli-info')

        created_at = datetime.now().strftime('%H:%M:%S')

        info = {
            'created_at': created_at,
            'open_at': created_at,
            'last_database': 'cookiedbcli-info'
        }

        self._cookiedb.add('/info', info)

    def update_last_open(self) -> None:
        open_at = datetime.now().strftime('%H:%M:%S')
        self._cookiedb.add('/info/open_at', open_at)

    def _permitted_cmd(self, cmd_string: str) -> bool:
        db_methods = [
            'open', 'create_database', 'add', 'close',
            'get', 'delete', 'checkout', 'update'
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

        if self._permitted_cmd(command):
            exec(f'result = {command}')
        else:
            raise exceptions.InvalidCommandError(f'Command "{command}" unknown')

        return locals()['result']
