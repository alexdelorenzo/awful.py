from sa_tools.poster import Poster
from sa_tools.base.sa_obj import SAObj
from sa_tools.parsers.post import PostParser


class Post(SAObj):
    def __init__(self, parent, id, content=None, **properties):
        super(Post, self).__init__(parent, id, content, **properties)

        self.poster = None
        self.body = ""
        self.date_posted = dict()
        self.user_info = dict()
        self.parser = PostParser(self)
        self.read()

    def __repr__(self):
        if self.body and self.poster:
            id, username = str(self.id), self.poster.name
            info_str = 'Post by ' + username

            return info_str

        else:
            return super(Post, self).__repr__()

    def __str__(self):
        return self.body

    def _add_poster(self, user_id, name, content):
        self.poster = Poster(self, id=user_id, content=content, name=name)

    def _set_results(self):
        self._apply_key_vals(self.parser.parse(self._content))
        self._add_poster(*self.user_info)

    def read(self):
        super(Post, self).read()

        self._set_results()
        self._delete_extra()


