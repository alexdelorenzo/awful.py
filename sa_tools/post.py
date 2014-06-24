from sa_tools.poster import SAPoster
from sa_tools.base.sa_obj import SAObj
from sa_tools.parsers.post import SAPostParser


class SAPost(SAObj):
    def __init__(self, parent, id, content=None, **properties):
        super(SAPost, self).__init__(parent, id, content, **properties)

        self.poster = None
        self.body = ""
        self.date_posted = dict()
        self.parser = SAPostParser(self)
        self.read()

    def __repr__(self):
        if self.body and self.poster:
            id, username = str(self.id), self.poster.name
            info_str = 'Reply #' + id + ' by ' + username

            return info_str

        else:
            return super(SAPost, self).__repr__()

    def __str__(self):
        return self.body

    def _add_poster(self, user_id, name, content):
        self.poster = SAPoster(self, id=user_id, content=content, name=name)

    def _set_results(self):
        self._add_poster(*self.parser.user_info)
        self.body = self.parser.body

    def read(self):
        super(SAPost, self).read()

        self.parser.parse()
        self._set_results()
        self._delete_extra()


