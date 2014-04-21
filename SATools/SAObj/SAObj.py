from SATools.SAObj.SAMagic import SAMagic
from SATools.SATypes import IntOrNone, TriggerProperty

from bs4 import BeautifulSoup


class SADynamic(object):
    def __init__(self, parent, **properties):
        self.parent = parent
        self._substitutes = dict()
        self._properties = properties
        self._dynamic_attr()

    def _delete_extra(self):
        """
        Second runner up.

        If unread, call this at the end of your overridden read()
        """
        significant_false_vals = False, 0, dict()
        delete_these = list(self.__dict__.items())

        for name, val in delete_these:
            is_falsy = not val
            is_special = val in significant_false_vals

            if is_falsy and not is_special:
                delattr(self, name)

    def _dynamic_attr(self):
        """
        Consolation prize.

        If unread, call this at the end of your overridden read()
        """
        if not self._properties:
            return

        for name, val in self._properties.items():
            if name in self._substitutes:
                name = self._substitutes[name]
            self._dynamic_property_read(name, val)

        #del self._properties

    def _dynamic_property(self, p_obj=None, name=None, fget=None, fset=None, val=None):
        if p_obj is None:
            p_obj = self

        new_name = '_' + name
        setattr(p_obj, new_name, val)

        if not fget:
            fget = lambda self: getattr(p_obj, new_name)

        if not fset:
            fset = lambda self, new_val: setattr(p_obj, new_name, new_val)

        prop_obj = property(fget, fset)
        setattr(p_obj.__class__, name, prop_obj)

    def _dynamic_property_read(self, name, val, condition=None):
        """
        This'll get refactored out in a much saner way.
        """
        new_name = '_' + name

        def fget(self):
            attr = getattr(self, new_name)
            is_unread = self.unread
            is_none = attr is None

            if is_unread and not attr:
                self.read()
                return getattr(self, new_name)

            return attr

        self._dynamic_property(name, fget=fget, val=val)


class SAObj(SAMagic, SADynamic):
    id = IntOrNone()

    def __init__(self, parent, id=None, content=None, name=None, url=None, **properties):
        super(SAObj, self).__init__(parent, **properties)
        self.id = id
        self.session = self.parent.session
        self._content = content
        self.name = name
        self._base_url = 'http://forums.somethingawful.com/'
        self.url = url if url else self._base_url

        self.unread = True
        self._reads = 0

        self._dynamic_attr()

    def _fetch(self, url=None):
        if not url:
            url = self.url

        response = self.session.get(url)

        if not response.ok:
            raise Exception(("There was an error with your request ",
                             url, response.status_code, response.reason))

        self._content = BeautifulSoup(response.content)

    def read(self, pg=1):
        """
        You need to call _dynamic_attr() and _delete_extra() for full
        sa_obj interop.

        If unread, call them at the end of your overridden read()
        """
        if self.unread:
            self.unread = False

        self._reads += 1


class SAListObj(SAObj):
    from SATools.SAParsers.SANaviParsers import SANaviParser

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

            navi = self.SANaviParser.parse_navi(self)
            self.navi = SAPageNavi(self, content=navi)

        self.navi.read(pg)

    def read(self, pg=1):
        super(SAListObj, self).read(pg)

        url = self.url + '&' + self._page_keyword + '=' + str(pg)
        self._fetch(url)
        self._setup_navi(pg)


class SAPageNavi(SAObj):
    from SATools.SAParsers.SANaviParsers import SAPageNaviParser

    page = IntOrNone()
    pages = IntOrNone(1)

    def __init__(self, *args, **properties):
        super(SAPageNavi, self).__init__(*args, **properties)
        self.parser = self.SAPageNaviParser(self)

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
