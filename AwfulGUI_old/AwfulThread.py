__author__ = 'alex'

from PyQt5 import QtWidgets
from AwfulGUI_old.AwfulPost import AwfulPost

class AwfulLongThread(QtWidgets.QWidget):
		def __init__(self, sa_thread, pg=1):
			super().__init__()
			self.layout = QtWidgets.QVBoxLayout(self)

			if not sa_thread.posts:
				sa_thread.read(pg)

			self.add_posts(sa_thread)

		def add_posts(self, sa_thread):
			for post_obj in sa_thread.posts.values():
				self.layout.addWidget(AwfulPost(post_obj))


class AwfulThread(QtWidgets.QScrollArea):
	def __init__(self, sa_thread, pg=1, **kwargs):
		super().__init__(**kwargs)
		self.setMaximumHeight(800)
		self.long_thread = AwfulLongThread(sa_thread, pg)
		self.setWidget(self.long_thread)


class AwfulThreadStackedWidget(QtWidgets.QStackedWidget):
	def __init__(self, sa_thread, pg=1):
		super().__init__()
		self.thread = AwfulThread(sa_thread, parent=self)
		self.addWidget(self.thread)
		self.setCurrentWidget(self.thread)

		self.addWidget(AwfulThread(sa_thread, pg=2, parent=self))


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