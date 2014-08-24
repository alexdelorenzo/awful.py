from sa_tools.base.sa_collection import SACollection
from sa_tools.base.descriptors import TriggerProperty
from sa_tools.parsers.thread import ThreadParser

from sa_tools.post import Post
from sa_tools.poster import Poster
from sa_tools.last_read import LastRead

from collections import OrderedDict


class Thread(SACollection):
    posts = TriggerProperty('read', 'posts')

    parser = ThreadParser()

    def __init__(self, parent, id, tr_thread=None, **properties):
        super().__init__(parent, id, content=tr_thread,
                                       page=1, **properties)
        self.url = self._base_url + '/showthread.php?threadid=' + str(self.id)
        self.posts = OrderedDict()
        self._apply_info()
        self.name = self.title

    def read(self, page=1):
        self.posts = OrderedDict()

        super().read(page)

        self._add_posts()
        self._delete_extra()

    def _add_post(self, post_id, post_content, is_op=False):
        sa_post = Post(self, post_id, post_content)
        self.posts[sa_post.id] = sa_post

        if is_op:
            self.author = sa_post.poster

    def _add_last_read(self, lr_content):
        self.last_read = LastRead(self, self.id, lr_content)

    def _add_author(self, user_id, name=None):
        self.author = Poster(self, user_id, name=name)

    def _apply_parsed_results(self, results):
        condition_map = {'author': expand(self._add_author),
                         'last_read': self._add_last_read}
        self._apply_key_vals(results, condition_map=condition_map)

    def _apply_info(self):
        info_gen = self.parser.gen_info(self._content)
        self._apply_parsed_results(info_gen)

    def _add_posts(self):
        post_gen = self.parser.gen_posts(self._content)

        for post_info in post_gen:
            self._add_post(*post_info)


def expand(func):
    def new(arg):
        return func(*arg)
    return new
