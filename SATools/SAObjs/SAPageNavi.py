from SATools.SAParsers.SANaviParsers import SAPageNaviParser
from SATools import SAObj, IntOrNone


class SAPageNavi(SAObj):
    page = IntOrNone()
    pages = IntOrNone(1)

    def __init__(self, *args, **properties):
        super(SAPageNavi, self).__init__(*args, **properties)
        self.parser = SAPageNaviParser(self)

    def __repr__(self):
        if self.parent.unread:
            return "Navi: unread parent_obj"

        return "Page " + str(self.page) + " of " + str(self.pages)

    def _modify_parent(self):
        self.parent.page = self.page
        self.parent.pages = self.pages

    def read(self, pg=1):
        super(SAPageNavi, self).read(pg)

        self.page = pg if pg <= self.pages else self.pages
        self.parser.parse()
        self._modify_parent()
        self._delete_extra()