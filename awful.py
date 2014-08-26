from sa_tools.base.magic import MagicMixin
from sa_tools.inbox import Inbox
from sa_tools.session import SASession
from sa_tools.index import Index

import os
import pickle
import sys


def py_ver() -> str:
    return str(sys.version_info.major)


class APSession(object):
    def __init__(self, username: str, passwd: str=None, save_session: bool=False, *args, **kwargs):
        self.username = username
        self.passwd = passwd
        self._session_bak = \
            '.' + username.replace(' ', '_') + py_ver() + '.bak'
        self.session = self._get_session(save_session=save_session)

        del passwd
        del self.passwd

    def _get_session(self, save_session: bool=True) -> SASession:
        backup_exists = os.path.exists(self._session_bak)
#        session = None

        if backup_exists:
            session = self._load_session()

        else:
            session = SASession(self.username, self.passwd)

            if save_session:
                self._save_session(session)

        return session

    def _load_session(self) -> None:
        with open(self._session_bak, 'rb') as old_session:
            print("Loading from backup: " + self._session_bak)
            session = pickle.load(old_session)

        return session

    def _save_session(self, session: SASession) -> None:
        with open(self._session_bak, 'wb') as session_file:
            pickle.dump(session, session_file)


class AwfulPy(APSession, MagicMixin):
    def __init__(self, username, *args, **kwargs):
        super().__init__(username, *args, **kwargs)
        self.index = Index(self.session)
        self.inbox = Inbox(self.session)

        self.name = "awful.py"
        self.version = "v0.2014.08.24"

    def __repr__(self):
        info = '[' + self.name + ' ' + self.version + '] '
        acct = 'Logged in as ' + self.username
        login_time = ' on ' + self.session.login_time
        return info + acct + login_time