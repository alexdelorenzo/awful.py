__author__ = 'alex'

from AwfulGUI.AwfulThread import AwfulThreadDocker as DockingThread
from AwfulGUI.AwfulForum import AwfulForumsList, AwfulThreadList
from AwfulGUI import AwfulForum
from PyQt5 import QtGui, QtWidgets

class AwfulIndex(QtWidgets.QMainWindow):
	def __init__(self, awful_py):
		super().__init__()
		self.setMinimumSize(500, 900)
		self.root = QtWidgets.QWidget(self)
		self.root.setMinimumSize(500, 900)
		self.awful_py = awful_py
		self.hbox_main = QtWidgets.QHBoxLayout(self.root)

		self.vbox_lists = _Vbox_Lists(awful_py)
		self.vbox_console = _Vbox_Console()

		self.organize_layout()


	def organize_layout(self):
		self.hbox_main.addWidget(self.vbox_lists)
		self.hbox_main.addWidget(self.vbox_console)


class _Gridbox_Threads(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.root = QtWidgets.QWidget(self)

		self.setMinimumSize(500, 500)
		self.layout = QtWidgets.QGridLayout(self.root)


class _Vbox_Lists(QtWidgets.QWidget):
	def __init__(self, awful_py):
		super().__init__()
		self.setMinimumWidth(240)
		self.layout = QtWidgets.QVBoxLayout(self)
		self.list_forums = AwfulForumsList(awful_py.index)
		self.list_threads = AwfulThreadList(awful_py.index.forums['219'])

		self.layout.addWidget(self.list_forums)
		self.layout.addWidget(self.list_threads)

class _Vbox_Console(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.layout = QtWidgets.QVBoxLayout(self)
		self.grid_threads = _Gridbox_Threads()
		self.button = AwfulPost()

		self.layout.addWidget(self.grid_threads)
		self.layout.addWidget(self.button)

class AwfulPost(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.setMaximumHeight(100)
		self.layout = QtWidgets.QHBoxLayout(self)
		self.text_box = QtWidgets.QPlainTextEdit(self)
		self.post_button = QtWidgets.QPushButton('Post', self)

		self.layout.addWidget(self.text_box)
		self.layout.addWidget(self.post_button)