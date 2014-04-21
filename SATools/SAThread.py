from collections import OrderedDict as ordered

from SATools.SAObjs.SAListObj import SAListObj
from SATools.SAObjs.SADescriptors import TriggerProperty
from SATools.SAPost import SAPost
from SATools.SAPoster import SAPoster
from SATools.SALastRead import SALastRead
from SATools.SAParsers.SAThreadParser import SAThreadParser


class SAThread(SAListObj):
    posts = TriggerProperty('read', 'posts')

    def __init__(self, parent, id, tr_thread=None, **properties):
        super(SAThread, self).__init__(parent, id, content=tr_thread, page=1, **properties)
        self.url = self._base_url + '/showthread.php?threadid=' + str(self.id)
        self.posts = ordered()

        self.parser = SAThreadParser(self)
        self.parser.parse_info()
        self.name = self.title

        self._dynamic_attr()

    def read(self, page=1):
        self.posts = ordered()

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

    def _add_author(self, user_id, name=None):
        sa_poster = SAPoster(self, user_id, name=name)
        self.author = sa_poster