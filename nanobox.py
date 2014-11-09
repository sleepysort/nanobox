#!/usr/bin/env python
import dropbox
import os, sys, time

from nanobox import credentials, filesystem, settings, sync

# Print version and usage information
def about():
    print 'Nanobox v' + settings.NANOBOX_VERSION
    print 'Usage: nanobox login|logout|mount <path>|status|sync'

def readSyncTime():
    try:
        with open(NANOBOX_PATHS['sync'], 'r') as f:
            return float(f.readline())
    except IOError:
        return 0

if __name__ == '__main__':
    # Check that valid arguments were passed
    if len(sys.argv) < 2:
        about()
        sys.exit(0)

    # Execute appropriate command
    if sys.argv[1] == 'mount':
        try:
            if len(sys.argv) == 3:
                mountpoint = filesystem.setMountPoint(sys.argv[2])
            else:
                mountpoint = filesystem.setMountPoint()
            print "Mount point set to " + mountpoint
        except IOError:
            print "Failed to set mountpoint."
            sys.exit(1)

    # Login
    elif sys.argv[1] == 'login':
        # Check to see if user is already logged in
        try:
            access_token, user_name = credentials.getCredentials()
            print "Already logged in as " + user_name + "."
            sys.exit(0)
        except credentials.NotLoggedInException:
            pass

        # Load app keys
        try:
            print settings.NANOBOX_PATHS['app_key']
            with open(settings.NANOBOX_PATHS['app_key'], 'r') as f:
                APP_KEY = f.readline().strip()
            with open(settings.NANOBOX_PATHS['app_secret'], 'r') as f:
                APP_SECRET = f.readline().strip()
        except IOError:
            print 'ERROR: ' + settings.NANOBOX_PATHS['app_key'] + ' or ' + \
                  settings.NANOBOX_PATHS['app_secret'] + ' is invalid.'
            sys.exit(1)

        # Begin authentication flow
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

        auth_url = flow.start()
        print 'Go to ' + auth_url + ' and login.'
        auth_code = raw_input('Enter the authorization code here: ').strip()
        access_token, user_id = flow.finish(auth_code)

        client = dropbox.client.DropboxClient(access_token)
        user_name = client.account_info()['display_name']

        # Store credentials in files
        credentials.login(access_token, user_name)

        # Success!
        print 'Successfully logged in as ' + user_name + '!'

    # Logout
    elif sys.argv[1] == 'logout':
        try:
            access_token, user_name = credentials.getCredentials()
            ans = raw_input('Logout? (Currently logged in as ' + user_name + ')[y/n] ')
            if ans == 'y':
                credentials.logout()
                print "Logout successful!"
        except credentials.NotLoggedInException:
            print "You are not currently logged in."
            sys.exit(0)

    # Check the status of files, logged in user, mount point, etc
    elif sys.argv[1] == 'status':
        # TODO: Implement
        try:
            access_token, user_name = credentials.getCredentials()
            print 'Currently logged in as ' + user_name + '.'
        except credentials.NotLoggedInException:
            print 'Not logged in.'

        try:
            mountpoint = filesystem.getMountPoint()
            print 'Mount point set to ' + mountpoint
        except credentials.NotLoggedInException:
            print 'No mount point set.'
            sys.exit(0)

        print filesystem.listAll()

    # Sync the files to Nanobox
    elif sys.argv[1] == 'sync':
        # TODO: Implement
        sync.synchronize(None)
        #with open(NANOBOX_PATHS['sync'], 'w+') as f:
        #    synctime = time.time()
        #    f.write(str(synctime))
        #    print "synced at " + str(synctime)

    # Invalid command; exit the program
    else:
        about()
        sys.exit(0)