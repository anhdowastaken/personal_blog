"""
Backs up db file to Dropbox.
"""

import os
import sys
import getopt
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

DB_HOST = 'localhost'
DB_USERNAME = 'personalblog'
DB_PASSWORD = '+vE9)_Ma+#w=Y[(x'
DB_NAME = 'personalblog'

LOCALFILE = 'personalblog.sql'
BACKUPPATH = '/personalblog.sql'

def backup_db():
    dumpcmd = "mysqldump -h {} -u'{}' -p'{}' {} > {}.sql".format(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME, DB_NAME)
    os.system(dumpcmd)

# Uploads contents of LOCALFILE to Dropbox
def backup_to_dropbox():
    with open(LOCALFILE, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")
        try:
            dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()

if __name__ == '__main__':
    argv = sys.argv[1:]

    token = ''
    try:
        opts, args = getopt.getopt(argv, "ht:", ["help", "token="])
    except getopt.GetoptError:
        print("backup_db.py --token <Dropbox token string>")
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("backup_db.py --token <Dropbox token string>")
            sys.exit()
        elif opt in ("-t", "--token"):
            token = arg

    # Check for an access token
    if (len(token) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token.")

    # Create an instance of a Dropbox class, which can make requests to the API.
    print("Creating a Dropbox object...")
    dbx = dropbox.Dropbox(token)

    # Check that the access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an "
            "access token from the app console on the web.")

    # Create a backup of the current settings file
    backup_db()
    backup_to_dropbox()

    print("Done!")
