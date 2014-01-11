__author__ = 'alex'
from satools_test import AwfulPyTest
from AwfulQML.AwfulThread import AwfulThreadModel

import unittest

from PyQt5 import QtCore, QtGui, QtWidgets, QtQml, QtQuick

class QMLTest(unittest.TestCase):
	def setUp(self):
		self.ap_test = AwfulPyTest()
		self.ap_test.setUp()
		self.ap_test.test_read_post()

	def tearDown(self):
		pass

	def test_atm(self):
		self.atm = AwfulThreadModel(self.ap_test.thread)

	def test_load_qml(self):
		self.atm = AwfulThreadModel(self.ap_test.thread)
		self.app = QtWidgets.QApplication(['',''])
		self.view = QtQuick.QQuickView()
		self.rc = self.view.rootContext()
		self.rc.setContextProperty('AwfulThreadModelObj', self.atm)

		self.view.setSource(QtCore.QUrl('AwfulQML/AwfulThread.qml'))
		self.view.setResizeMode(1)

		self.view.show()

if __name__ == '__main__':
	unittest.main()
