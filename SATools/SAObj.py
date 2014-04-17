from SATools.SATypes import IntOrNone

from bs4 import BeautifulSoup


class SAMagic(object):
    def __init__(self, parent, **properties):
        #super(SAMagic, self).__init__()
        self.parent = parent

    def __repr__(self):
        if self.name:
            return self.name
        else:
            return super(SAMagic, self).__repr__()

    def __str__(self):
        if self.name:
            return self.__repr__()
        else:
            return super(SAMagic, self).__str__()

    def __getattr__(self, attr):
        """
        Monkey patch of the year, 2014.

        See _delete_extra() for why this exists.
        If I'm not being paid I'm going to have fun.
        """
        if attr not in self.__dict__:
            return None

    def __setattr__(self, key, value):
        super(SAMagic, self).__setattr__(key, value)


class SADynamic(object):
    def __init__(self, parent, **properties):
        #super(SADynamic, self).__init__()
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

    def _dynamic_property(self, name, fget=None, fset=None, val=None):
        new_name = '_' + name
        setattr(self, new_name, val)

        if not fget:
            fget = lambda self: getattr(self, new_name)

        if not fset:
            fset = lambda self, new_val: setattr(self, new_name, new_val)

        prop_obj = property(fget, fset)
        setattr(self.__class__, name, prop_obj)

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
        del id  # sorry builtins' namespace :(
        self.session = self.parent.session
        self._content = content
        self.name = name
        self.base_url = 'http://forums.somethingawful.com/'
        self.url = url if url else self.base_url

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
    page = IntOrNone()
    pages = IntOrNone()

    def __init__(self, *args, **properties):
        self.page = 1
        self.pages = 1
        self.navi = None

        self._collection = None
        self._children = None
        self._page_keyword = 'pagenumber'
        self._substitutes = \
            {'collection': '_collection',
             'children': '_children'}
        super(SAListObj, self).__init__(*args, **properties)

    def _setup_navi(self, pg=1):
        if not self.navi:
            navi = self._content.find('div', 'pages')
            self.navi = SAPageNavi(self, content=navi)

        self.navi.read(pg)

    def read(self, pg=1):
        super(SAListObj, self).read(pg)

        url = self.url + '&' + self._page_keyword + '=' + str(pg)
        self._fetch(url)
        self._setup_navi(pg)


class SAPageNavi(SAObj):
    page = IntOrNone()
    pages = IntOrNone()

    def __init__(self, *args, **properties):
        super(SAPageNavi, self).__init__(*args, **properties)

        self.page = 1
        self.pages = 1

    def __repr__(self):
        if self.parent.unread:
            return "Navi: unread parent_obj"

        return "Page " + str(self.page) + " of " + str(self.pages)

    def _modify_parent(self):
        self.parent.page = self.page
        self.parent.pages = self.pages

    def _parse_page_selector(self):
        page_selector = self._content.find_all('option')

        if len(page_selector):
            self.pages = page_selector[-1].text
        else:
            self.pages = 1

    def read(self, pg=1):
        super(SAPageNavi, self).read(pg)

        self.page = pg if pg <= self.pages else self.pages
        self._parse_page_selector()
        self._modify_parent()
        self._delete_extra()