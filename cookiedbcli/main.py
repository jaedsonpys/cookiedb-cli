import getpass
import readline
from pprint import pprint

import cookiedb

from .__init__ import __version__
from .dbcli import CookieDBCLI
from .exceptions import InvalidCommandError


def main():
    dbcli = CookieDBCLI()
    databases = dbcli.get_databases()

    try:
        if databases:
            while True:
                password = getpass.getpass('Password: ')
                dbcli.configure(password)

                test_db = databases[0].replace('.cookiedb', '')
                
                try:
                    dbcli.execute(f'db.open("{test_db}")')
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
    except KeyboardInterrupt:
        print('Bye.')
        exit(0)

    print('\033[34mWelcome to CookieDB CLI!')
    print('See the complete CookieDB documentation at https://github.com/jaedsonpys/cookiedb')
    print(f'\n* CookieDB CLI version: {__version__}')
    print(f'* CookieDB version: {cookiedb.__version__}\033[m\n')

    while True:
        open_db = dbcli.execute('db.checkout()')
        command = input(f'\033[34mcookiedb\033[m (\033[1;32m{open_db}\033[m) > ')

        try:
            result = dbcli.execute(command)
        except InvalidCommandError:
            result = '\033[31mUnknown CookieDB command.\033[m'
        except cookiedb.exceptions.DatabaseExistsError:
            result = '\033[31mThis database already exists\033[m'
        except cookiedb.exceptions.DatabaseNotFoundError:
            result = '\033[31mThis database was not found\033[m'
        except cookiedb.exceptions.NoOpenDatabaseError:
            result = '\033[31mNo open databases\033[m'
        except cookiedb.exceptions.InvalidDatabaseKeyError:
            result = '\033[31mInvalid key for accessing the database\033[m'

        if result and isinstance(result, (dict, list)):
            print('\033[1;32m')
            pprint(result)
            print('\033[m')
        elif result and isinstance(result, (str, int, float)):
            print(f'\033[1;32m{result}\033[m')
