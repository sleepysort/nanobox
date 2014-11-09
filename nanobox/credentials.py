"""
Nanobox credentials module. Handles login, logout, and file 
read/write for credentials.

*Currently using files to store access token and session credentials. 
 Look into mmap for future versions.
"""

import os

from nanobox import settings


# Exception that is raised when login credentials are not found
class NotLoggedInException(Exception):
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return repr(self.msg)


# Logs user in with given credentials (saves credentials to filepath)
def login(access_token, user_name):
    with open(settings.NANOBOX_PATHS['credentials'], 'w+') as f:
        f.write(access_token + '\n')
        f.write(user_name)


# Logs user out (deletes filepath)
def logout():
    if not os.path.isfile(settings.NANOBOX_PATHS['credentials']):
        raise NotLoggedInException("User is not logged in.")
    os.remove(settings.NANOBOX_PATHS['credentials'])


# Reads the credentials from file
def getCredentials():
    try:
        with open(settings.NANOBOX_PATHS['credentials'], 'r') as f:
            access_token = f.readline().strip()
            user_name = f.readline().strip()
            return (access_token, user_name)
    except IOError:
        raise NotLoggedInException("User is not logged in.")