from sa_tools.parsers.thread import ThreadParser
from sa_tools.base.list_obj import SACollection
from sa_tools.base.descriptors import TriggerProperty

from sa_tools.post import Post
from sa_tools.poster import Poster
from sa_tools.last_read import LastRead

from collections import OrderedDict as ordered

from fn import _


class Thread(SACollection):
    posts = TriggerProperty('read', 'posts')

    def __init__(self, parent, id, tr_thread=None, **properties):
        super(Thread, self).__init__(parent, id, content=tr_thread,
                                       page=1, **properties)
        self.url = self._base_url + '/showthread.php?threadid=' + str(self.id)
        self.posts = ordered()

        self.parser = ThreadParser(self)
        self.parser.parse_info()
        self.name = self.title

        self._dynamic_attr()

    def read(self, page=1):
        self.posts = ordered()

        super(Thread, self).read(page)

        self.parser.parse()
        self._set_results()
        self._delete_extra()

    def _add_post(self, post_id, post_content, is_op=False):
        sa_post = Post(self, post_id, post_content)
        post_id = sa_post.id

        self.posts[post_id] = sa_post

        if is_op:
            poster = sa_post.poster
            self.author = poster

    def _add_last_read(self, lr_content, lr=None):
        print('lr1')
        if lr_content:
            lr = LastRead(self, self.id, lr_content)
            print('lr')

        self.last_read = lr

    def _add_author(self, user_id, name=None):
        sa_poster = Poster(self, user_id, name=name)
        self.author = sa_poster

    def _apply_parsed_results(self):
        condition_map = {'author': expand(self._add_author),
                         'last_read': self._add_last_read}

        super(Thread, self)._apply_parsed_results(condition_map=condition_map)

    def _set_results(self):
        post_gen = self.parser.post_gen

        for post_info in post_gen:
            self._add_post(*post_info)

        self._apply_parsed_results()


def expand(func):
    def new(arg):
        func(*arg)
    return new
