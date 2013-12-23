__author__ = 'alex'
from SATools.SASession import SASession
from SATools.SAIndex import SAIndex


class AwfulPy(object):
	def __init__(self, username, passwd):
		self.username = username

		self.session = SASession(username, passwd)
		self.index = SAIndex(self.session)

		del passwd

def main():
	pass


if __name__ == "__main__":
	main()