# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nerp.ui'
#
# Created: Mon Dec 23 22:26:13 2013
#      by: PyQt5 UI code generator 5.0.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.POSTING = QtWidgets.QWidget(MainWindow)
        self.POSTING.setObjectName("POSTING")
        self.tabs = QtWidgets.QTabWidget(self.POSTING)
        self.tabs.setGeometry(QtCore.QRect(0, 10, 791, 471))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabs.sizePolicy().hasHeightForWidth())
        self.tabs.setSizePolicy(sizePolicy)
        self.tabs.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabs.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabs.setObjectName("tabs")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabs.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabs.addTab(self.tab_2, "")
        self.textbox = QtWidgets.QPlainTextEdit(self.POSTING)
        self.textbox.setGeometry(QtCore.QRect(30, 487, 641, 71))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textbox.sizePolicy().hasHeightForWidth())
        self.textbox.setSizePolicy(sizePolicy)
        self.textbox.setObjectName("textbox")
        self.post = QtWidgets.QPushButton(self.POSTING)
        self.post.setGeometry(QtCore.QRect(680, 490, 101, 61))
        self.post.setObjectName("post")
        MainWindow.setCentralWidget(self.POSTING)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        self.menuConnect = QtWidgets.QMenu(self.menubar)
        self.menuConnect.setObjectName("menuConnect")
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLogin = QtWidgets.QAction(MainWindow)
        self.actionLogin.setObjectName("actionLogin")
        self.actionLogout = QtWidgets.QAction(MainWindow)
        self.actionLogout.setObjectName("actionLogout")
        self.actionSet_refresh_rate_don_t_get_this_banned = QtWidgets.QAction(MainWindow)
        self.actionSet_refresh_rate_don_t_get_this_banned.setObjectName("actionSet_refresh_rate_don_t_get_this_banned")
        self.menuConnect.addAction(self.actionLogin)
        self.menuConnect.addAction(self.actionLogout)
        self.menuOptions.addAction(self.actionSet_refresh_rate_don_t_get_this_banned)
        self.menubar.addAction(self.menuConnect.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(MainWindow)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.post.setText(_translate("MainWindow", "PushButton"))
        self.menuConnect.setTitle(_translate("MainWindow", "Connect"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.actionLogin.setText(_translate("MainWindow", "Login"))
        self.actionLogout.setText(_translate("MainWindow", "Logout"))
        self.actionSet_refresh_rate_don_t_get_this_banned.setText(_translate("MainWindow", "Set refresh rate (don\'t get this banned)"))

