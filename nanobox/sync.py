"""
Nanobox synchronization module. Handles synchronization API calls and read/write
for synchronization data.
"""

import dropbox

import os
import cPickle as pickle
from nanobox import credentials, settings

# Synchronize local files with cloud files
def synchronize(localfiles):
    try:
        access_token, user_name = credentials.getCredentials()
        client = dropbox.client.DropboxClient(access_token)
        cloudfiles = set()
        getCloudFiles(client, cloudfiles, '/')
        
    except credentials.NotLoggedInException:
        raise

# Populates result set with paths to all files in user's Dropbox
def getCloudFiles(client, result, root):
    data = client.metadata(root)
    contents = data['contents']
    for c in contents:
        if c['is_dir']:
            getCloudFiles(client, result, c['path'])
        else:
            result.add(c['path'])

# Get the time of the last sync
def getSyncTime():
    try:
        with open(settings.NANOBOX_PATHS['synctime'], 'r') as f:
            return float(f.readline())
    except IOError:
        return 0


# Update the time of last sync
def setSyncTime(synctime):
    with open(settings.NANOBOX_PATHS['synctime'], 'w+') as f:
        f.write(str(synctime))


# Return the set of files that were last synced.
def getSyncFiles():
    try:
        syncfiles = pickle.load(open(settings.NANOBOX_PATHS['syncfiles'], 'rb')) 
        return syncfiles
    except:
        return set()

# Updates the set of files that have been synced.
def setSyncFiles(syncfiles):
    pickle.dump(syncfiles, open(settings.NANOBOX_PATHS['syncfiles'], 'wb+'))