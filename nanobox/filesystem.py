"""
Nanobox filesystem module. Handles all local filesystem related 
operations.
"""

import os

import cPickle as pickle
from nanobox import settings


# Exception that is raised when mount point is invalid
class InvalidMountPointException(Exception):
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return repr(self.msg)


# Sets the mount point for Nanobox. Saves to file. Creates directories
# if necessary. Returns path of mount point.
def setMountPoint(mountpath="~/Nanobox"):
    mountpath += "/"
    with open(settings.NANOBOX_PATHS['mountpoint'], 'w+') as f:
        mountpath = os.path.dirname(os.path.expanduser(mountpath))
        if not os.path.exists(mountpath):
            try:
                os.mkdir(mountpath)
            except Exception:
                raise IOError()
        f.write(mountpath)
    return mountpath


# Gets the mount point from file.
def getMountPoint():
    try:
        with open(settings.NANOBOX_PATHS['mountpoint'], 'r') as f:
            mountpath = f.readline().strip()
            if not os.path.exists(mountpath):
                raise InvalidMountPointException("Invalid mount path.")
            else:
                return mountpath
    except IOError:
        raise InvalidMountPointException("Invalid mount path.")


# Returns a set of all files in the mount point (including those
# in subfolders).
def listAll():
    try:
        result = set()
        topdir = getMountPoint()
        for root, dirs, files in os.walk(topdir):
            root = "/" + root[len(topdir) + 1:]  # bit of a hack; fix this
            for name in files:
                result.add(os.path.join(root, name))
        return result
    except InvalidMountPointException:
        raise

# Returns a set of all files that have been modified since the last
# sync.
def listChanged():
    try:
        topdir = getMountPoint()
        synctime = getSyncTime()
        syncfiles = getSyncFiles()
        localfiles = listAll()
        modified = set()
        newfiles = set()

        for f in localfiles:
            localpath = topdir + f
            if os.path.getmtime(os.path.join(localpath)) > synctime:
                modified.add(f)
            elif f not in syncfiles:
                newfiles.add(f)
        return (modified, newfiles)
    except InvalidMountPointException:
        raise


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