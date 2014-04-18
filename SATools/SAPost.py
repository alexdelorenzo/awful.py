from SATools.SAPoster import SAPoster
from SATools.SAObj import SAObj


class SAPost(SAObj):
    def __init__(self, parent, id, content=None, **properties):
        super(SAPost, self).__init__(parent, id, content, **properties)
        self.poster = None
        self.body = ""
        self.read()

    def __repr__(self):
        if self.body and self.poster:
            return 'Reply #' + str(self.id) + ' by ' + self.poster.name
        else:
            return super(SAPost, self).__repr__()

    def __str__(self):
        return self.body

    def _parse_from_thread(self):
        user_id = self._content.td['class'].pop()[7:]
        user_name = self._content.dt.text

        content = self._content.find('td', 'userinfo')
        self.poster = SAPoster(self, user_id, content, name=user_name)

        has_post = self._content.find('td', 'postbody')
        self.body = has_post.text.strip() if has_post else ""

    def read(self):
        super(SAPost, self).read()
        self._parse_from_thread()
        self._delete_extra()