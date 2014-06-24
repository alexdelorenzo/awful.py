from sa_tools.base.sa_obj import SAObj
from sa_tools.parsers.poster import ProfileParser


class Poster(SAObj):
    def __init__(self, parent, id=None, content=None, name=None, **properties):
        super(Poster, self).__init__(parent, id, content=content, name=name, **properties)
        self.avatar_url = None
        self.title = None
        self.reg_date = None

        self.post_count = None
        self.post_rate = None
        self.last_post = None
        self.contact_info = dict({})

        self.parser = ProfileParser(self)
        self._delete_extra()

        if self.id:
            self.url = "https://forums.somethingawful.com/member.php?action=getinfo&userid=" + str(self.id)

    def read(self):
        super(Poster, self).read()
        self.parser.parse()
        self._delete_extra()