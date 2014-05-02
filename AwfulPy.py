from SATools.SAObjs.SAMagic import SAMagic
from SATools.SASession import SASession
from SATools.SAIndex import SAIndex

import os, pickle, sys


class APSession(object):
    def __init__(self, username, passwd=None, save_session=False, *args, **kwargs):
        self.username = username
        self.passwd = passwd
        self.session_bak = \
            '.' + username.replace(' ', '_') + self._py_ver() + '.bak'
        self.session = self._load_session(save_session)

        del passwd
        del self.passwd

    def _load_session(self, save_session=True):
        backup_exists = os.path.exists(self.session_bak)
#        session = None

        if backup_exists:
            with open(self.session_bak, 'rb') as old_session:
                print("Loading from backup: " + self.session_bak)
                session = pickle.load(old_session)
                print("Finished loading from backup.")

        else:
            session = SASession(self.username, self.passwd)

            if save_session:
                self._save_session(session)

        return session

    def _save_session(self, session):
        with open(self.session_bak, 'wb') as session_file:
            pickle.dump(session, session_file)

    def _py_ver(self):
        return str(sys.version_info.major)


class AwfulPy(APSession, SAMagic):
    def __init__(self, username, *args, **kwargs):
        super(AwfulPy, self).__init__(username, *args, **kwargs)
        self.index = SAIndex(self.session)
        self.name = "AwfulPy"
        self.version = "v20140421"

    def __repr__(self):
        basic = self.name + ' ' + self.version + '.\n'
        acct = 'Logged in as ' + self.username
        since = ' since ' + self.session.logged_in_at
        return basic + acct + since