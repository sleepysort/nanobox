"""
Nanobox synchronization module. Handles synchronization API calls and read/write
for synchronization data.
"""

import dropbox

import os, time
from nanobox import credentials, filesystem, settings

# Synchronize local files with cloud files. Takes set of files to push,
# updates cloudfiles to be the set of files pulled
def synchronize(localfiles, cloudfiles):
    try:
        mountpoint = filesystem.getMountPoint()
        access_token, user_name = credentials.getCredentials()
        client = dropbox.client.DropboxClient(access_token)
        
        # Push all locally modified files to Dropbox
        for p in localfiles:
            localpath = mountpoint + p
            f = open(localpath, 'rb')
            client.put_file(p, f, True)

        # Pull cloud files not yet in local
        getCloudFiles(client, cloudfiles, '/')
        cloudcopy = set(cloudfiles)
        localfiles = filesystem.listAll()
        for p in cloudcopy:
            if p not in localfiles:
                localpath = mountpoint + p
                c = client.get_file(p)
                with open(localpath, 'w+') as f:
                    f.write(c.read())
            else:
                cloudfiles.remove(p)
        
        filesystem.setSyncTime(time.time())
        time.sleep(1)
        filesystem.setSyncFiles(filesystem.listAll())
    except:
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