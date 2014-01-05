__author__ = 'alex'
from SATools.SAForum import SAForum


class SASection(SAForum):
	def __init__(self, id, session, name=None, subforums=dict(), parent=None):
		super(SASection, self).__init__(id, session, name=name, subforums=subforums, parent=parent)

		if not self.subforums:
			self.read()

		self.forums = self.subforums
		self.threads = self.forums


def main():
	pass


if __name__ == "__main__":
	main()