from sa_tools import SAObj
from sa_tools.parsers.pm import PMParser


class PM(SAObj):
    parser = PMParser()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.url = "http://forums.somethingawful.com/private.php"

        info_gen = self.parser.parse(self._content)
        self._apply_key_vals(info_gen)