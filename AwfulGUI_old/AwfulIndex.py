__author__ = 'alex'

from PyQt5 import QtGui, QtWidgets, QtCore
from AwfulGUI_old.AwfulThread import AwfulThreadDocker as DockingThread
from AwfulGUI_old.AwfulForum import AwfulForumsList, AwfulThreadList
from AwfulGUI_old import AwfulForum
from AwfulGUI_old.AwfulSlots import AwfulSlots


class AwfulIndex(QtWidgets.QMainWindow):
	def __init__(self, awful_py):
		super().__init__()
		self.awful_py = awful_py

		self.root = QtWidgets.QWidget()
		self.setMinimumSize(1200, 800)
		self.root.setMinimumSize(1200, 800)
		self.hbox_main = QtWidgets.QHBoxLayout(self.root)

		self.setCentralWidget(self.root)

		self.vbox_lists = _Vbox_Lists(awful_py)
		self.vbox_console = _Vbox_Console()

		self.size_policy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

		self.setup_sizes()
		self.organize_layout()

		self.slots = AwfulSlots(self)

	def setup_sizes(self):
		self.setSizePolicy(self.size_policy)
		self.root.setSizePolicy(self.size_policy)

		self.vbox_console.setSizePolicy(self.size_policy)
		self.vbox_console.grid_threads.setSizePolicy(self.size_policy)

	def organize_layout(self):
		self.hbox_main.addWidget(self.vbox_lists)
		self.hbox_main.addWidget(self.vbox_console)


class _Gridbox_Threads(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.root = QtWidgets.QWidget(self)

		self.setMinimumSize(1000, 600)
		self.layout = QtWidgets.QGridLayout(self.root)


class _Vbox_Lists(QtWidgets.QWidget):
	def __init__(self, awful_py):
		super().__init__()
		self.size_policy = QtWidgets.QSizePolicy()
		self.layout = QtWidgets.QVBoxLayout(self)

		self.list_forums = AwfulForumsList(awful_py.index)
		self.list_threads = AwfulThreadList(awful_py.index.forums['202'])

		self.setup_sizes()

	def setup_sizes(self):
		self.setMinimumWidth(240)
		self.setMaximumWidth(240)

		self.size_policy.setHorizontalPolicy(QtWidgets.QSizePolicy.Maximum)
		self.size_policy.setVerticalPolicy(QtWidgets.QSizePolicy.Expanding)

		self.setSizePolicy(self.size_policy)
		self.list_forums.setSizePolicy(self.size_policy)
		self.list_threads.setSizePolicy(self.size_policy)

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
		self.layout = QtWidgets.QHBoxLayout(self)
		self.text_box = QtWidgets.QPlainTextEdit(self)
		self.post_button = QtWidgets.QPushButton('Post', self)

		self.layout.addWidget(self.text_box)
		self.layout.addWidget(self.post_button)