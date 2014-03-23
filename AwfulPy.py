from SATools.SASession import SASession
from SATools.SAIndex import SAIndex
import os, pickle, sys

class AwfulPy(object):
    def __init__(self, username, passwd=None, save_session=True):
        py_version = str(sys.version_info.major)
        self.username = username
        self.passwd = passwd
        self.session_bak = \
            '.' + username.replace(' ', '_') + py_version + '.bak'
        self.session = self._load_session(save_session)
        self.index = SAIndex(self.session)

        del passwd
        del self.passwd

    def _load_session(self, save_session=True):
        backup_exists = os.path.exists(self.session_bak)
        session = None

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


def main():
    pass


if __name__ == "__main__":
    main()
