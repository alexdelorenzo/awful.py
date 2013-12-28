__author__ = 'alex'
from SATools.SASession import SASession
from SATools.SAIndex import SAIndex
import os, pickle

class AwfulPy(object):
	def __init__(self, username, passwd=None):
		self.username = username
		self.passwd = passwd

		self.session_bak = '.' + username + '_sa.bak'
		self.session = self._load_session()

		self.index = SAIndex(self.session)

		del passwd
		del self.passwd

	def _load_session(self):
		backup_exists = os.path.exists(self.session_bak)
		session = None

		if backup_exists:
			with open(self.session_bak, 'rb') as old_session:
				print("Loading from backup: " + self.session_bak)
				session = pickle.load(old_session)

		else:
			session = SASession(self.username, self.passwd)
			self._save_session(session)

		return session

	def _save_session(self, session):
		with open(self.session_bak, 'wb') as session_file:
			pickle.dump(session, session_file)





def main():
	pass


if __name__ == "__main__":
	main()