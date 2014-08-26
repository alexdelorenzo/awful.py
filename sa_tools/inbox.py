from sa_tools import SAObj
from sa_tools.base.descriptors import TriggerProperty
from sa_tools.parsers.inbox import InboxParser
from sa_tools.pm import PM

from collections import OrderedDict


class Inbox(SAObj):
    name = 'PM Inbox'
    pms = TriggerProperty('read', 'pms')

    parser = InboxParser()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.url = "http://forums.somethingawful.com/private.php"
        self.pms = OrderedDict()

    def __repr__(self):
        desc = self.name

        if not self.unread:
            count, unread_count = self._get_counts()
            desc += ': [' + str(unread_count) + ' unread messages of '
            desc += str(count) + ' total]'

        return desc

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
            self._add_pm(pm)

    def _get_counts(self) -> (int, int):
        count = len(self.pms)
        unread_count = len([pm for pm in self.pms.values() if pm.unread])

        return count, unread_count