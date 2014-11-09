nanobox
=======

A custom Dropbox client. Compresses data prior to syncronization to reduce space usage on the user side.

Setup Instructions
------------------

1. Make sure you have Python 2.7 installed and correctly setup in your `PATH`.
2. [Download](https://bootstrap.pypa.io/get-pip.py) and install `pip`.
3. Run `pip install dropbox`. You may need to use `sudo`.
4. Done! Run `nanobox.py` to use Nanobox.

Notes
-----

- This application is not intended for widespread usage. This was mainly an experiment in using the Dropbox APIs.
- The compression module is not yet done. Next thing on the list.
- You need the Dropbox application key and secret key in the `.keys/APP_KEY` and `.keys/APP_SECRET` files (respectively) for Nanobox to work. I have not uploaded my own keys for obvious reasons.
- Do not manually modify any files in the `.config` folder. The application is not guaranteed to work if those files are tampered with.