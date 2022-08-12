import getpass
import readline
from pprint import pprint

import cookiedb

from .__init__ import __version__
from .dbcli import CookieDBCLI


def main():
    dbcli = CookieDBCLI()
    databases = dbcli.get_databases()

    while True:
        password = getpass.getpass('Password: ')
        dbcli.configure(password)

        if databases:
            test_db = databases[0].replace('.cookiedb', '')
            
            try:
                dbcli.execute(f'db.open("{test_db}")')
            except cookiedb.exceptions.InvalidDatabaseKeyError:
                print('\033[32mWrong password, try again\033[m')
            else:
                break
        else:
            break
