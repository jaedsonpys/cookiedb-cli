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

import getpass
import readline
from pprint import pprint

import cookiedb

from .__init__ import __version__
from .dbcli import CookieDBCLI
from .exceptions import InvalidCommandError


def main() -> int:
    dbcli = CookieDBCLI()
    databases = dbcli.get_databases()

    try:
        if databases:
            while True:
                password = getpass.getpass('Password: ')
                dbcli.configure(password)
                
                try:
                    dbcli.execute(f'db.open("cookiedbcli-info")')
                except cookiedb.exceptions.InvalidDatabaseKeyError:
                    print('\033[31mWrong password, try again\033[m')
                else:
                    break
        else:
            print('Set a password for access to the database')
            password = getpass.getpass('Password: ')
            
            while True:
                confirm_password = getpass.getpass('Confirm password: ')
                if password != confirm_password:
                    print('\033[31mPasswords are not equal. Try again\033[m')
                else:
                    break

            dbcli.configure(password)
            dbcli.create_info_database()
    except KeyboardInterrupt:
        print('Bye.')
        return 0

    dbcli.update_last_open()
    dbcli.execute('db.close()')

    print('\033[34mWelcome to CookieDB CLI!')
    print('See the complete CookieDB documentation at https://github.com/jaedsonpys/cookiedb')
    print(f'\n* CookieDB CLI version: {__version__}')
    print(f'* CookieDB version: {cookiedb.__version__}\033[m\n')

    while True:
        try:
            open_db = dbcli.execute('db.checkout()') or 'no open database'
            command = input(f'cookiedb ({open_db}) > ').strip()

            if command == 'exit':
                print('\nBye.')
                return 0
            elif command == 'list':
                for i in dbcli.get_databases():
                    print(f'\033[1;32m{i.replace(".cookiedb", "")}\033[m')

                continue

            try:
                result = dbcli.execute(command)
            except InvalidCommandError:
                result = '\033[33mUnknown CookieDB command.\033[m'
            except NameError:
                result = '\033[33mDo not try to run external code here!\033[m'
            except cookiedb.exceptions.DatabaseExistsError:
                result = '\033[31mThis database already exists\033[m'
            except cookiedb.exceptions.DatabaseNotFoundError:
                result = '\033[31mThis database was not found\033[m'
            except cookiedb.exceptions.NoOpenDatabaseError:
                result = '\033[31mNo open databases\033[m'
            except cookiedb.exceptions.InvalidDatabaseKeyError:
                result = '\033[31mInvalid key for accessing the database\033[m'
            except cookiedb.exceptions.ItemNotExistsError:
                result = '\033[31mNon-existent path\033[m'

            if result and isinstance(result, (dict, list)):
                print('\033[1;32m')
                pprint(result)
                print('\033[m')
            elif result and isinstance(result, (str, int, float)):
                print(f'\033[1;32m{result}\033[m')
        except KeyboardInterrupt:
            print('\nBye.')
            return 0
