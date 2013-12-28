__author__ = 'alex'
from PyQt5 import QtGui, QtWidgets, QtCore
from SATools import SAPost


class QtPost(QtWidgets.QTextBrowser):
	def __init__(self, post_obj):
		super().__init__()
		self.doc = QtGui.QTextDocument(post_obj.body)
		self.setDocument(self.doc)
		self.setMinimumHeight(10)
		#self.setMaximumHeight(80)

class QtTar(QtWidgets.QLabel):
	def __init__(self, poster_obj):
		super().__init__()
		self.setText(poster_obj.name + ":")



class AwfulPost(QtWidgets.QWidget):
	def __init__(self, post_obj):
		super().__init__()
		self.layout = QtWidgets.QVBoxLayout(self)
		self.tar = QtTar(post_obj.poster)
		self.post = QtPost(post_obj)

		self.layout.addWidget(self.tar)
		self.layout.addWidget(self.post)


def main():
	pass


if __name__ == "__main__":
	main()