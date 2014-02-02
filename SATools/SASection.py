__author__ = 'alex'
from SATools.SAForum import SAForum


class SASection(SAForum):
	def __init__(self, id, session, content=None, parent=None, name=None, subforums=dict()):
		super(SASection, self).__init__(id, session, content, parent, name, subforums=subforums)

		if not self.subforums:
			self.read()

		self.forums = self.subforums
		self.threads = self.forums


def main():
	pass


if __name__ == "__main__":
	main()