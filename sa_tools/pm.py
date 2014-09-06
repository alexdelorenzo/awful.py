from sa_tools.parsers.pm import PMParser
from sa_tools.post import Post


class PM(Post):
    _base_url = "http://forums.somethingawful.com/private.php"
    parser = PMParser()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_info()
        self.url = \
            "http://forums.somethingawful.com/private.php" + \
            "?action=show&privatemessageid=" + str(self.id)

    def _apply_info(self):
        info_gen = self.parser.parse(self._content)
        self._apply_key_vals(info_gen)
