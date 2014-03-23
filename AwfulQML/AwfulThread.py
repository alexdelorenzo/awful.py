from PyQt5.QtCore import QAbstractListModel
from PyQt5 import QtCore, QtGui
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

        if self.data.last_read:
            self._last_read = \
                LastReadWrapper(self.data.last_read, self)
        else:
            self._last_read = False

    def _wrap_posts(self):
        self.posts = \
            [AwfulPostQWrapper(post)
             for post in self.data.posts.values()]

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.posts)

    def roleNames(self):
        return {0: 'post'}

    def data(self, index, role=0):
        if index.isValid():
            return self.posts[index.row()]

    @pyqtProperty(QtCore.QObject, constant=True)
    def last_read(self):
        return self._last_read

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

    @pyqtProperty(bool, constant=True)
    def has_lr(self):
        return bool(self.data.last_read)

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




class LastReadWrapper(QWrapper):
    def __init__(self, lr_obj, parent):
        super().__init__(lr_obj)
        self.data.read()
        self.parent = parent

    @pyqtProperty(str, constant=True)
    def lastpost(self):
        return self.data.url_last_post

    @pyqtProperty(str, constant=True)
    def unread_pages(self):
        return self.data.unread_pages

    @pyqtProperty(str, constant=True)
    def unread_count(self):
        return self.data.unread_count

    @pyqtProperty(str, constant=True)
    def lastread_off(self):
        return self.data.url_switch_off

    @QtCore.pyqtSlot(int)
    def read(self, pg=1):
        self.data.read(pg)

    @QtCore.pyqtSlot()
    def jump(self):
        self.parent.read_page(int(self.parent.data.pages) - int(self.data.unread_pages))

    @QtCore.pyqtSlot()
    def stop(self):
        self.data.stop_tracking()



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

