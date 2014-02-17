from PyQt5.QtCore import QAbstractListModel
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtProperty, pyqtSlot

from AwfulQML.AwfulForum import ForumModel


class IndexModel(QAbstractListModel):
    def __init__(self, index):
        super().__init__()
        self.forums = []
        self.data = index.forums
        self._wrap_forums()

    def _wrap_forums(self):
        for forum in self.data.values():
            self.forums.append(ForumModel(forum))

    def rowCount(self, parent):
        return len(self.forums)

    def roleNames(self):
        return {0: 'forum'}

    def data(self, index, role=0):
        if index.isValid():
            return self.forums[index.row()]

    @pyqtProperty(str, constant=True)
    def title(self):
        return self.data.name

    @pyqtProperty(str, constant=True)
    def title(self):
        return self.data.name

    @pyqtProperty(bool, constant=True)
    def has_lr(self):
        return False