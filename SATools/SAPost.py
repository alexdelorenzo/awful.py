from SATools.SAPoster import SAPoster
from SATools.SAObj import SAObj


class SAPost(SAObj):
    def __init__(self, parent, id, content=None, **properties):
        super(SAPost, self).__init__(parent, id, content, **properties)
        self.unread = True
        self.url = ""

        user_id = self._content.td['class'].pop()[7:]
        user_name = self._content.dt.text

        content = self._content.find('td', 'userinfo')
        self.poster = SAPoster(self, user_id, content, name=user_name)

        if self._content:
            has_post = self._content.find('td', 'postbody')
            self.body = has_post.text.strip() if has_post else ""
            self.unread = False

        self._delete_extra()

    def read(self):
        self.unread = False
        for td in self._content.find_all('td'):
            if td['class'] == 'userinfo':
                for dd in td.find_all('dd'):
                    pass
        raise NotImplemented()


def main():
    pass


if __name__ == "__main__":
    main()
