__author__ = 'alex'
from PyQt5 import QtWidgets, QtCore


class AwfulForumsList(QtWidgets.QListWidget):
	def __init__(self, sa_index):
		super().__init__()

		self.forums = []

		for forum in sa_index.forums.values():
			list_obj = AwfulForumItem(forum)
			self.forums.append(list_obj)
			self.addItem(list_obj)


class AwfulForumItem(QtWidgets.QListWidgetItem):
	def __init__(self, sa_forum):
		super().__init__()
		self.forum = sa_forum
		self.setText(sa_forum.name)
		self.setToolTip(sa_forum.name)
		self.setSizeHint(QtCore.QSize(200, 12))


class AwfulThreadList(QtWidgets.QListWidget):
	def __init__(self, sa_forum):
		super().__init__()

		if not sa_forum.threads:
			sa_forum.read()

		self.setWordWrap(True)
		self.threads = []

		for thread in sa_forum.threads.values():
			list_obj = AwfulThreadItem(thread)
			self.threads.append(list_obj)
			self.addItem(list_obj)


class AwfulThreadItem(QtWidgets.QListWidgetItem):
	def __init__(self, sa_thread):
		super().__init__()

		self.thread = sa_thread
		self.setText(sa_thread.name)
		self.setToolTip(sa_thread.name)
		self.setSizeHint(QtCore.QSize(200, 12))


def main():
	pass


if __name__ == "__main__":
	main()