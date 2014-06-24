from sa_tools.parsers.search_result import SearchResultParser
from sa_tools.base import SAObj
from sa_tools.thread import Thread
from sa_tools.forum import Forum
from sa_tools.poster import Poster
from sa_tools.post import Post


class SASearchResult(SAObj):
    def __init__(self, parent=None, id=None, name=None, content=None, **properties):
        super(SASearchResult, self).__init__(parent, id, name=name, content=content, **properties)
        self.header = self.parent._table_header
        self.parser = SearchResultParser(self)
        self.forum = None
        self.poster = None
        self.views = None
        self.date = None
        self.post = None
        self.thread = None

    def read(self):
        self.parser.parse()
        self.unread = False
        del self._columns

    def _add_forum(self, forum_id, forum_name):
        self.forum = Forum(self, forum_id, name=forum_name)

    def _add_poster(self, user_id, username):
        self.poster = Poster(self, user_id, name=username)

    def _add_post(self, post_id, post_content):
        self.post = Post(self, post_id, post_content)

    def _add_thread(self, thread_id, thread_name):
        self.thread = Thread(self, thread_id, thread_name)