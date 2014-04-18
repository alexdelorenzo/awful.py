from SATools.SAObj import SAListObj
from SATools.SATypes import TriggerProperty
from SATools.SAParser import SAThreadParser
from SATools.SAPost import SAPost
from SATools.SALastRead import SALastRead

from collections import OrderedDict as ordered


class SAThread(SAListObj):
    posts = TriggerProperty('read', 'posts')

    def __init__(self, parent, id, tr_thread=None, **properties):
        super(SAThread, self).__init__(parent, id, content=tr_thread, page=1, **properties)
        self.base_url = "http://forums.somethingawful.com/"
        self.url = self.base_url + '/showthread.php?threadid=' + str(self.id)
        self.parser = SAThreadParser(self, tr_thread=tr_thread)
        self.parser.parse()

        self._dynamic_attr()
        self.name = self.title
        self.posts = ordered()

    def read(self, page=1):
        super(SAThread, self).read(page)

        self.parser.parse()
        self._delete_extra()

    def _add_post(self, post_id, post_content):
        sa_post = SAPost(self, post_id, post_content)
        post_id = sa_post.id

        self.posts[post_id] = sa_post

    def _add_last_read(self, lr_content, lr=None):
        if lr_content:
            lr = SALastRead(self, self.id, lr_content)

        self.last_read = lr
