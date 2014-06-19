from SATools.SAPoster import SAPoster
from SATools.base.sa_obj import SAObj
from SATools.SAParsers.SAPostParser import SAPostParser


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

        else:
            info_str = super(SAPost, self).__repr__()

        return info_str

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


