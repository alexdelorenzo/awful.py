__author__ = 'alex'

from PyQt5 import QtWidgets
from AwfulGUI.AwfulPost import AwfulPost

class AwfulLongThread(QtWidgets.QWidget):
		def __init__(self, sa_thread):
			super().__init__()
			self.layout = QtWidgets.QVBoxLayout(self)

			if not sa_thread.posts:
				sa_thread.read()

			self.add_posts(sa_thread)

		def add_posts(self, sa_thread):
			for post_obj in sa_thread.posts.values():
				self.layout.addWidget(AwfulPost(post_obj))


class AwfulThread(QtWidgets.QScrollArea):
	def __init__(self, sa_thread):
		super().__init__()
		self.setMaximumHeight(800)
		self.long_thread = AwfulLongThread(sa_thread)
		self.setWidget(self.long_thread)


class AwfulThreadDocker(QtWidgets.QDockWidget):
	def __init__(self, sa_thread):
		super().__init__(sa_thread.name)
		self.setMaximumSize(400,300)
		self.thread = AwfulThread(sa_thread)
		self.setWidget(self.thread)


def main():
	pass

if __name__ == "__main__":
	main()