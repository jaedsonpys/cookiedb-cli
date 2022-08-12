import getpass
import readline
from pprint import pprint

import cookiedb

from .__init__ import __version__
from .dbcli import CookieDBCLI


def main():
    dbcli = CookieDBCLI()
    databases = dbcli.get_databases()

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
