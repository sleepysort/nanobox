"""
Nanobox synchronization module. Handles synchronization API calls and read/write
for synchronization data.
"""

import dropbox

import os, gzip, shutil, time
from nanobox import credentials, filesystem, settings

# Synchronize local files with cloud files. Takes set of files to push.
# Returns set of pulled filenames and Dropbox space usage via queue.
def synchronize(localfiles, queue):
    try:
        mountpoint = filesystem.getMountPoint()
        access_token, user_name = credentials.getCredentials()
        client = dropbox.client.DropboxClient(access_token)
        
        buffer_path = os.path.join(mountpoint + '/', '.buffer')
        os.mkdir(buffer_path)

        # Push all locally modified files to Dropbox
        for p in localfiles:
            if not os.path.exists(os.path.dirname(buffer_path + p)):
                os.makedirs(os.path.dirname(buffer_path + p))
            localpath = mountpoint + p
            f_u = open(localpath, 'rb')
            f_z = gzip.open(buffer_path + p, 'wb')
            f_z.writelines(f_u)
            f_u.close()
            f_z.close()
            with open(buffer_path + p, 'rb') as f:
                client.put_file(p, f, True)
            os.remove(buffer_path + p)

        # Pull cloud files not yet in local
        cloudfiles = set()
        total_size = getCloudFiles(client, cloudfiles, '/')
        cloudcopy = set(cloudfiles)
        localfiles = filesystem.listAll()[0]
        for p in cloudcopy:
            if p not in localfiles:
                if not os.path.exists(os.path.dirname(buffer_path + p)):
                    os.makedirs(os.path.dirname(buffer_path + p))
                localpath = mountpoint + p
                c = client.get_file(p)
                with open(buffer_path + p, 'w+') as f:
                    f.write(c.read())
                f_z = gzip.open(buffer_path + p, 'rb')
                if not os.path.exists(os.path.dirname(localpath)):
                    os.makedirs(os.path.dirname(localpath))
                f_u = open(localpath, 'wb')
                f_u.write(f_z.read())
                f_u.close()
                f_z.close()
                os.remove(buffer_path + p)
            else:
                cloudfiles.remove(p)
        shutil.rmtree(buffer_path)
        
        queue.put(cloudfiles)
        queue.put(total_size)
        filesystem.setSyncTime(time.time())
        time.sleep(1)
        filesystem.setSyncFiles(filesystem.listAll()[0])
    except:
        raise
    finally:
        if os.path.exists(buffer_path):
            shutil.rmtree(buffer_path)

# Populates result set with paths to all files in user's Dropbox, and
# returns the total size (space used)
def getCloudFiles(client, result, root):
    data = client.metadata(root)
    contents = data['contents']
    size = 0
    for c in contents:
        if c['is_dir']:
            size += getCloudFiles(client, result, c['path'])
        else:
            result.add(c['path'])
            size += c['bytes']
    return size