#
# Program to interact with Dropbox and support sending/retrieving files
#
# Author: David Bryant (djbryant@gmail.com)
# Version: 1.0
# Date: March 3, 2013

import os
import argparse

from dropbox import client, rest, session
from os.path import expanduser

PROG_NAME = 'kribensis'
APP_KEY = 'INSERT_APP_KEY_HERE'
APP_SECRET = 'INSERT_APP_SECRET_HERE'
ACCESS_TYPE = 'app_folder' # Either 'dropbox' or 'app_folder' as configured for the app


# Use Dropbox Session but extend it to support storing the access token in a
# file on disk for easy subsequent use.
class StoredSession(session.DropboxSession):
    """a wrapper around DropboxSession that stores a token to a file on disk"""
    TOKEN_FILE = "~/kribensis_tokens.txt"

    def load_creds(self):
        """Load access credentials from storage file and attach them to current session"""
        try:
            stored_creds = open(os.path.expanduser(self.TOKEN_FILE)).read()

            self.set_token(*stored_creds.split('|'))
            print "[loaded access token]"
        except IOError:
            pass # don't worry if it's not there

    def write_creds(self, token):
        """Write access credentials from per-user storage file"""
        f = open(os.path.expanduser(self.TOKEN_FILE), 'w')
        f.write("|".join([token.key, token.secret]))
        f.close()

    def delete_creds(self):
        os.unlink(self.os.path.expanduser(self.TOKEN_FILE))

    def link(self):
        """Generate access credentials so application can connect to user's Dropbox account"""
        print "Linking to Dropbox..."
        request_token = self.obtain_request_token()
        url = self.build_authorize_url(request_token)
        print "url:", url
        print "Please authorize in the browser. After you're done, press enter."
        raw_input()

        self.obtain_access_token(request_token)
        self.write_creds(self.token)

    def unlink(self):
        self.delete_creds()
        self.DropboxSession.unlink(self)

    # Upload a local file to Dropbox
    def do_put(self,local,remote):
        """Upload a local file to Dropbox"""
        print "Upload local file '{}' to Dropbox file '{}'".format(local,remote)
        from_file = open(os.path.expanduser(local),"rb")
        self.api_client.put_file(self.current_path + "/" + remote, from_file)

    # Download a file from Dropbox
    def do_get(self,remote,local):
        """Download a remote file from Dropbox to the local system"""
        print "Download Dropbox file '{}' to local file '{}'".format(remote,local)
        to_file = open(os.path.expanduser(local),"wb")
        f, metadata = self.api_client.get_file_and_metadata(self.current_path + "/" + remote)
        print "Metadata: {}".format(metadata)
        to_file.write(f.read())

    # List files in the current directory
    def do_ls(self):
        """List files in the current remote directory"""
        print "Contents of directory 'Apps/{}/{}':".format(PROG_NAME,self.current_path)
        resp = self.api_client.metadata(self.currrent_path)

        if 'contents' in resp:
            for f in resp['contents']:
                name = os.path.basename(f['path'])
                encoding = locale.getdefaultlocale()[1]
                print "%s".format(name.encode(encoding))

    # Move/rename a remote file or directory
    def do_mv(self, from_path, to_path):
        """Move/rename a remote file or directory"""
        print "Move/rename remote file '{}' to '{}'".format(from_path,to_path)
        self.api_client.file_move(self.current_path + "/" + from_path,
                                  self.currnet_path + "/" + to_path)


# Main routine for standalone operation as a command line utility
def main():
    # Create the argument parser
    parser = argparse.ArgumentParser()

    # Arguments supported
    #  -a,--authorize                 executes the Dropbox authentical process & creates an access token
    #  -put local_file remote_file    sends file from local host to Dropbox
    #  -get remote_file local_file    retrieves file from Dropbox to local host
    #  -move source dest              move/rename a remote file or directory
    #  -l,--list                      lists files in current remote directory

    parser.add_argument("-a","--authorize",help="Execute interactive Dropbox authentication process",
            action="store_true")
    parser.add_argument("-put",nargs=2,help="Send file from local host to Dropbox")
    parser.add_argument("-get",nargs=2,help="Retrieve file from Dropbox to local host")
    parser.add_argument("-move",nargs=2,help="Move/rename a remote file or directory")
    parser.add_argument("-l","--list",help="Lists files in current remote directory")


    # Parse command line arguments
    args = parser.parse_args()


    # Check for application keys to validate this app with Dropbox
    if APP_KEY == '' or APP_SECRET == '':
        exit("You need to set your APP_KEY and APP_SECRET!")

    # Here's the logic of connecting to Dropbox for file transfer
    #
    # 1. Create a session for us to use via the StoredSession object. This also provides
    #    access to a set of session-oriented functions via StoredSession
    # 2. Create a DropboxClient object, which is how we access and invoke the Dropbox API
    # 3. Attempt to read a Dropbox access token from a per-user storage file that can
    #    persist across uses of this application.  If the token exists then bind it
    #    to our session so we can interact with Dropbox.  In Dropbox parlance a session 
    #    with a valid access token is said to be "linked" to the user's account.  There
    #    may not be a storage file, in which case the session remains "unlinked".
    # 4. If we've been asked (via the --authorize command line option) to authorize the 
    #    user then do so via the link() function in the session.  This interacts with the 
    #    user so they can go to a special URL generated by link(), log into Dropbox, and 
    #    grant permission for this application to access their account.  An access token
    #    is generated by this process, which we'll store for future use.
    # 5. If we haven't been asked to authenticate then check to see if the session is
    #    "linked", which means we've been able to load a valid access token in step 3 above.
    #    If the session isn't linked then the user needs to go through the special
    #    authentication sequence by invoking this command with the --authorize option.
    # 6. At this point we have a working session which is "linked" through a valid access
    #    token and can issue Dropbox commnands using the API via the DropboxClient object.


    # Create Dropbox session & load stored credentials, which if present will "link" the session
    sess = StoredSession(APP_KEY,APP_SECRET,access_type=ACCESS_TYPE)
    sess.api_client = client.DropboxClient(sess)
    sess.current_path = ''
    sess.load_creds()

    # Should we authenticate (generating a stored token)? If so, do that first
    if(args.authorize):
        try:
            sess.link()
        except rest.ErrorResponse, e:
            exit("Error: {}".format(str(e)))

    else:
        if not sess.is_linked():
            exit("You must complete Dropbox authentication first.  Run '{} --authorize'".format(PROG_NAME))
        
    # Are we sending (uploading) files?
    if(args.put):
        sess.do_put(args.put[0],args.put[1])

    # Are we getting (downloading) files?
    if(args.get):
        sess.do_get(args.get[0],args.get[1])

    # Are we moving/renaming remote files?
    if(args.move):
        sess.do_mv(args.move[0],args.move[1])



if __name__ == '__main__':
    main()
