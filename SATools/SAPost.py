from SATools.SAPoster import SAPoster
from SATools.SAObj import SAObj
from SATools.SAParser import SAPostParser


class SAPost(SAObj):
    def __init__(self, parent, id, content=None, **properties):
        super(SAPost, self).__init__(parent, id, content, **properties)
        self.poster = None
        self.body = ""
        self.parser = SAPostParser(self)
        self.read()

    def __repr__(self):
        if self.body and self.poster:
            return 'Reply #' + str(self.id) + ' by ' + self.poster.name
        else:
            return super(SAPost, self).__repr__()

    def __str__(self):
        return self.body

    def _add_poster(self, user_id, name, content):
        self.poster = SAPoster(self, user_id, content, name=name)

    def read(self):
        super(SAPost, self).read()
        self.parser.parse()
        self._delete_extra()