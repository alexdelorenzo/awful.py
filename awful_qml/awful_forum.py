from PyQt5.QtCore import QAbstractListModel
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtProperty, pyqtSlot

from awful_qml.awful_thread import AwfulThreadModel


class ForumModel(QAbstractListModel):
    def __init__(self, forum):
        super().__init__()
        self.threads = []
        self.data = forum


    def _wrap_threads(self):
        if self.threads:
            threads = []
            for new_index, (thread_id, thread_obj) in enumerate(self.data.threads.items()):
                for index, thread in enumerate(self.threads):
                    old_thread_found = thread_id == thread.id
                    if False:
                        self.beginMoveRows(index, index, self, new_index)
                        threads.append(thread)
                        self.endMoveRows()
                        break
                else:
                    threads.append(AwfulThreadModel(thread_obj))
            self.threads = threads
        else:
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

    @pyqtProperty(bool, constant=True)
    def has_lr(self):
        return False

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