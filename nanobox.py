#!/usr/bin/env python
import dropbox
import os, sys

# Version number
NANOBOX_VERSION = '0.1'

# Paths to configuration files
NANOBOX_PATHS = {
	'mount': os.path.join(os.path.dirname(__file__), '.config/mountpoint'),
	'credentials': os.path.join(os.path.dirname(__file__), '.config/credentials'),
	'app_key': os.path.join(os.path.dirname(__file__), '.keys/APP_KEY'),
	'app_secret': os.path.join(os.path.dirname(__file__), '.keys/APP_SECRET'),
	'default_mountpoint': '~/Nanobox/',
}

# Print version and usage information
def about():
	print 'Nanobox v' + NANOBOX_VERSION
	print 'Usage: nanobox login|logout|mount <path>|status|sync'

# Read user access token
def readCredentials():
	try:
		with open(NANOBOX_PATHS['credentials'], 'r') as f:
			access_token = f.readline()
			user_name = f.readline()
			return (access_token, user_name)
	except IOError:
		print 'You are not logged in or your session has expired.'
		print 'Try logging in again.'
		exit(1)

# Read mount point path from file
def readMount():
	try:
		with open(NANOBOX_PATHS['mount'], 'r') as f:
			return f.readline()
	except IOError:
		print 'ERROR: ' + NANOBOX_PATHS['mount'] + ' does not exist or is corrupted'
		print 'Try deleting the file, then  $ nanobox mount'
		exit(1)


if __name__ == '__main__':
	# Check that valid arguments were passed
	if len(sys.argv) < 2:
		about()
		sys.exit(0)

	# Execute appropriate command
	if sys.argv[1] == 'mount':
		with open(NANOBOX_PATHS['mount'], 'w+') as f:
			if len(sys.argv) == 3 and os.path.exists(sys.argv[2]) and os.path.isdir(sys.argv[2]):
				f.write(sys.argv[2])
				print 'Mount point set to ' + sys.argv[2]
			else:
				mountpath = os.path.dirname(os.path.expanduser(NANOBOX_PATHS['default_mountpoint']))
				if not os.path.exists(mountpath):
					os.mkdir(mountpath)
					print "Created new directory at " + NANOBOX_PATHS['default_mountpoint']
				f.write(NANOBOX_PATHS['default_mountpoint'])
				print 'Mount point set to ' + NANOBOX_PATHS['default_mountpoint']

	# Login
	elif sys.argv[1] == 'login':
		# Check to see if user is already logged in
		if os.path.isfile(NANOBOX_PATHS['credentials']):
			access_token, user_name = readCredentials()       ###DRY A
			print 'Currently logged in as ' + user_name + '.'
			sys.exit(0)

		# Load app keys
		try:
			with open(NANOBOX_PATHS['app_key'], 'r') as f:
				APP_KEY = f.readline().strip()
			with open(NANOBOX_PATHS['app_secret'], 'r') as f:
				APP_SECRET = f.readline().strip()
		except IOError:
			print 'ERROR: ' + NANOBOX_PATHS['app_key'] + ' or ' + NANOBOX_PATHS['app_secret'] + ' is invalid.'
			exit(1)

		# Begin authentication flow
		flow = dropbox.client.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

		auth_url = flow.start()
		print 'Go to ' + auth_url + ' and login.'
		auth_code = raw_input('Enter the authorization code here: ').strip()
		access_token, user_id = flow.finish(auth_code)

		client = dropbox.client.DropboxClient(access_token)
		user_name = client.account_info()['display_name']

		# Store credentials in files
		with open(NANOBOX_PATHS['credentials'], 'w+') as f:
			f.write(access_token + '\n')
			f.write(user_name)

		# Success!
		print 'Successfully logged in as ' + user_name + '!'

	# Logout
	elif sys.argv[1] == 'logout':
		access_token, user_name = readCredentials()
		ans = raw_input('Logout (Currently logged in as ' + user_name + ')? [y/n] ')
		if ans == 'y':
			os.remove(NANOBOX_PATHS['credentials'])
			print "Logout successful!"

	# Check the status of files, logged in user, mount point, etc
	elif sys.argv[1] == 'status':
		# TODO: Implement
		access_token, user_name = readCredentials()        ###DRY A
		print 'Currently logged in as ' + user_name + '.'

	# Sync the files to Nanobox
	elif sys.argv[1] == 'sync':
		# TODO: Implement
		pass

	# Invalid command; exit the program
	else:
		about()
		sys.exit(0)
