from sa_tools.base.sa_obj import SAObj
from sa_tools.base.descriptors import TriggerProperty, IntOrNone
from sa_tools.base.page_navi import PageNavi
from sa_tools.parsers.navi import NaviParser


class SACollection(SAObj):
    page = IntOrNone()
    pages = IntOrNone(1)
    navi = TriggerProperty('read', 'navi')

    def __init__(self, *args, **properties):
        self._collection = None
        self._children = None
        self._page_keyword = 'pagenumber'
        self._substitutes = \
            {'collection': '_collection',
             'children': '_children'}
        super(SACollection, self).__init__(*args, **properties)

    def _setup_navi(self, pg=1):
        if not self.navi:
            navi_content = NaviParser.parse_navi(self)
            self.navi = PageNavi(self, content=navi_content)

        self.navi.read(pg)

    def _index_to_pg(self, pg):
        """
        Translates pg param to conform to a positive pg number.

        Handles negative page numbers to act like negative indices in lists.
        """

        negative_index = pg < 0

        if negative_index:
            if not self.pages:
                self.read()

            pg = self.pages + (pg + 1)

        return pg

    def read(self, pg=1):
        pg = self._index_to_pg(pg)

        super(SACollection, self).read(pg)

        url = self.url + '&' + self._page_keyword + '=' + str(pg)
        self._fetch(url)
        self._setup_navi(pg)
