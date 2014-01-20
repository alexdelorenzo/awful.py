from PyQt5.QtCore import QAbstractListModel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtProperty


class QWrapper(QtCore.QObject):
	"""This was pointless"""
	def __init__(self, data):
		super().__init__()
		self.data = data


class AwfulThreadModel(QAbstractListModel):
	def __init__(self, sa_thread):
		super().__init__()
		self.sa_thread = sa_thread
		self.data = self.sa_thread
		self.posts = []
		#self._wrap_posts()

	def _wrap_posts(self):
		self.posts = \
			[AwfulPostQWrapper(post) for post in self.data.posts.values()]

	def rowCount(self, parent=QtCore.QModelIndex()):
		return len(self.posts)

	def roleNames(self):
		return {0: 'post'}

	def data(self, index, role=0):
		if index.isValid():
			return self.posts[index.row()]

	@pyqtProperty(str, constant=True)
	def page(self):
		return str(self.data.page)

	@pyqtProperty(str, constant=True)
	def pages(self):
		return str(self.data.pages)

	@pyqtProperty(str, constant=True)
	def title(self):
		return self.data.title

	@pyqtProperty(str, constant=True)
	def id(self):
		return self.data.id

	@QtCore.pyqtSlot(int)
	def read_page(self, pg=1):
		self.beginResetModel()
		self.data.read(pg)
		self._wrap_posts()
		self.endResetModel()

	@QtCore.pyqtSlot()
	def next_page(self):
		pg = int(self.data.page) + 1
		self.read_page(pg)

	@QtCore.pyqtSlot()
	def prev_page(self):
		pg = int(self.data.page) - 1
		self.read_page(pg)

	@QtCore.pyqtSlot()
	def first_page(self):
		self.read_page(1)

	@QtCore.pyqtSlot()
	def last_page(self):
		self.read_page(self.pages)

	@QtCore.pyqtSlot(str)
	def reply(self, post_body):
		self.data.session.reply(self.data.id, post_body)
		self.last_page()
		

class AwfulPostQWrapper(QWrapper):
	def __init__(self, sa_post):
		super().__init__(sa_post)
		self.post = self.data

	@pyqtProperty(str, constant=True)
	def body(self):
		return self.post.body

	@pyqtProperty(str, constant=True)
	def content(self):
		return str(self.post.content.find('td', 'postbody'))

	@pyqtProperty(str, constant=True)
	def poster(self):
		return self.post.poster.name


def main():
	pass


if __name__ == "__main__":
	main()