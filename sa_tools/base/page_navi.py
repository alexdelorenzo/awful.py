from sa_tools.base.sa_obj import SAObj
from sa_tools.base.descriptors import IntOrNone
from sa_tools.parsers.page_navi import PageNaviParser


class PageNavi(SAObj):
    page = IntOrNone()
    pages = IntOrNone(1)

    parser = PageNaviParser(parent=None)

    def __init__(self, *args, **properties):
        super().__init__(*args, **properties)
        self._from_parent()

    def __repr__(self):
        if self.parent.unread:
            return "Navi: unread parent_obj"

        return "Page " + str(self.page) + " of " + str(self.pages)

    def _modify_parent(self):
        self.parent.page = self.page
        self.parent.pages = self.pages

    def _from_parent(self):
        self.page = self.parent.page
        self.pages = self.parent.pages

    def read(self, pg: int=1):
        super().read(pg)

        self.page = pg if pg <= self.pages else self.pages
        self.pages = self.parser.parse(self._content)

        self._modify_parent()
        self._delete_extra()


class ImmutablePageNavi(PageNavi):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def read(*args, **kwargs):
        pass

