from collections import OrderedDict
from sa_tools import SAObj
from sa_tools.parsers.inbox import InboxParser
from sa_tools.pm import PM


class Inbox(SAObj):
    parser = InboxParser()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.url = "http://forums.somethingawful.com/private.php"
        self.pms = OrderedDict()

    def read(self, pg: int=1):
        self._fetch()
        super().read(pg)

        self.pms = OrderedDict()

        info_gen, pm_gen = self.parser.parse(self._content)
        #self._apply_key_vals(info_gen)
        self._add_pms(pm_gen)

    def _add_pm(self, pm_content):
        pm = PM(content=pm_content)
        self.pms[pm.id] = pm

    def _add_pms(self, pm_gen: iter):
        for pm in pm_gen:
            print(pm)
            self._add_pm(pm)