nanobox
=======

A custom Dropbox client. Compresses data prior to syncronization to reduce space usage on the user side.

Setup Instructions
------------------

1. Make sure you have Python 2.7 installed and correctly setup in your `PATH`.
2. [Download](https://bootstrap.pypa.io/get-pip.py) and install `pip`.
3. Run `pip install dropbox`. You may need to use `sudo`.
4. [Download](https://github.com/sleepysort/nanobox/archive/master.zip) Nanobox.
5. Done! Run `nanobox.py` to use Nanobox.

** You must add a Dropbox application key and secret key in the `.keys/` directory for the application to work. See notes. **

Notes
-----

- This application is not intended for widespread usage. This was mainly an experiment in using the Dropbox APIs.
- You need the Dropbox application key and secret key in the `.keys/APP_KEY` and `.keys/APP_SECRET` files (respectively) for Nanobox to work. I have not uploaded my own keys for obvious reasons.
- Do not manually modify any files in the `.config` folder. The application is not guaranteed to work if those files are tampered with.
- The application will pull new files, but will not pull modified files in the cloud. Delete the local copy, then sync again.