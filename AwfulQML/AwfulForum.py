from PyQt5.QtCore import QAbstractListModel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtProperty, pyqtSlot

from AwfulThread import AwfulThreadModel


class ForumModel(QAbstractListModel):
	def __init__(self, forum):
		super().__init__()
		self.threads = []
		self.data = forum

	def _wrap_threads(self):
		self.threads = \
			[AwfulThreadModel(thread) 
			 for thread in self.data.threads.values()]

	def rowCount(self, parent):
		return len(self.threads)

	def roleNames(self):
		return {0: 'thread'}

	def data(self, index, role=0):
		if index.isValid():
			return self.threads[index.row()]

	@pyqtSlot(int)
	def read_page(self, pg=1):
		self.beginResetModel()
		self.data.read(pg)
		self._wrap_threads()
		self.endResetModel()

	@pyqtProperty(str, constant=True)
	def page(self):
		return str(self.data.page)

	@pyqtProperty(str, constant=True)
	def pages(self):
		return str(self.data.pages)

	@pyqtProperty(str, constant=True)
	def title(self):
		return self.data.name

	@pyqtProperty(str, constant=True)
	def id(self):
		return self.data.id

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