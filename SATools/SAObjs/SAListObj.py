from SATools import SAObj, IntOrNone
from SATools.SAObjs.SADescriptors import TriggerProperty
from SATools.SAObjs.SAPageNavi import SAPageNavi
from SATools.SAParsers.SANaviParsers import SANaviParser


class SAListObj(SAObj):
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
        super(SAListObj, self).__init__(*args, **properties)

    def _setup_navi(self, pg=1):
        if not self.navi:
            navi = SANaviParser.parse_navi(self)
            self.navi = SAPageNavi(self, content=navi)

        self.navi.read(pg)

    def read(self, pg=1):
        super(SAListObj, self).read(pg)

        url = self.url + '&' + self._page_keyword + '=' + str(pg)
        self._fetch(url)
        self._setup_navi(pg)