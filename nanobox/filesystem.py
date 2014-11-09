"""
Nanobox filesystem module. Handles all local filesystem related 
operations.
"""

import os

from nanobox import settings, sync


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
            root = root[len(topdir):]  # bit of a hack; fix this
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
        synctime = sync.getSyncTime()
        syncfiles = sync.getSyncFiles()
        result = listAll()

        for f in result:
            if os.path.getmtime(os.path.join(topdir + '/', f)) > synctime or \
               f not in syncfiles:
                result.remove(f)
        return result
    except InvalidMountPointException:
        raise