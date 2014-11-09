# Settings for Nanobox

import os

# Version number
NANOBOX_VERSION = '0.1'

# Paths to configuration files
NANOBOX_PATHS = {
    'app_key': os.path.join(os.path.dirname(__file__), '../.keys/APP_KEY'),
    'app_secret': os.path.join(os.path.dirname(__file__), '../.keys/APP_SECRET'),
    'credentials': os.path.join(os.path.dirname(__file__), '../.config/credentials'),
    'mountpoint': os.path.join(os.path.dirname(__file__), '../.config/mountpoint'),
    'synctime': os.path.join(os.path.dirname(__file__), '../.config/synctime'),
    'syncfiles': os.path.join(os.path.dirname(__file__), '../.config/syncfiles'),
}