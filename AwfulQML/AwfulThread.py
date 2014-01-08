from PyQt5.QtCore import QAbstractListModel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtProperty


class AwfulThreadModel(QAbstractListModel):
	def __init__(self, sa_thread):
		super().__init__()
		self.sa_thread = sa_thread
		self.posts = []
		self.parse_thread()

	def parse_thread(self):
		self.posts = \
			[AwfulPostQWrapper(post) for post in self.sa_thread.posts.values()]

	def rowCount(self, parent=QtCore.QModelIndex()):
		return len(self.posts)

	def roleNames(self):
		return {0: 'post'}

	def data(self, index, role=0):
		if index.isValid():
			return self.posts[index.row()]

	@pyqtProperty(str)
	def page(self):
		return str(self.sa_thread.page)

	@QtCore.pyqtSlot(int)
	def read_page(self, pg=1):
		self.beginResetModel()
		self.sa_thread.read(pg)
		self.parse_thread()
		self.endResetModel()

	@QtCore.pyqtSlot()
	def next_page(self):
		pg = self.sa_thread.page + 1
		self.read_page(pg)

	@QtCore.pyqtSlot()
	def prev_page(self):
		pg = self.sa_thread.page - 1
		self.read_page(pg)


class AwfulPostQWrapper(QtCore.QObject):
	def __init__(self, sa_post):
		super().__init__()
		self.post = sa_post

	@pyqtProperty(str)
	def body(self):
		return self.post.body

	@pyqtProperty(str)
	def content(self):
		return str(self.post.content.find('td', 'postbody'))

	@pyqtProperty(str)
	def poster(self):
		return self.post.poster.name


def main():
	pass


if __name__ == "__main__":
	main()