from PyQt5.QtCore import QAbstractListModel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtProperty

class AwfulThreadModel(QAbstractListModel):
	def __init__(self, sa_thread):
		super().__init__()
		self.posts = \
			[AwfulPostQWrapper(post) for post in sa_thread.posts.values()]

	def rowCount(self, parent=QtCore.QModelIndex()):
		return len(self.posts)

	def roleNames(self):
		return {0: 'post'}

	def data(self, index, role=0):
		if index.isValid():
			return self.posts[index.row()]

class AwfulPostQWrapper(QtCore.QObject):
	def __init__(self, sa_post):
		super().__init__()
		self.post = sa_post

	@pyqtProperty(str)
	def body(self):
		return self.post.body

	@pyqtProperty(str)
	def poster(self):
		return self.post.poster.name


def main():
	pass


if __name__ == "__main__":
	main()