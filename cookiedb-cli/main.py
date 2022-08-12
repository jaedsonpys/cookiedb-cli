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
