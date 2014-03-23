from bs4 import BeautifulSoup


class SAObj(object):
    """
    The gloves are off. It's a fucking free for all.
    """
    def __init__(self, parent, id=None, content=None, name=None, url=None, **properties):
        super(SAObj, self).__init__()

        self.parent = parent
        self.session = self.parent.session

        self.id = id
        self._content = content
        self.name = name
        self.url = url
        self._properties = properties

        self.unread = True
        self.base_url = None

        self._dynamic_attr()

    def __getstate__(self):
        """Down the rabbithole, fixes pickle hiccup b/c of __getattr__ override"""
        return self.__dict__

    def __setstate__(self, state):
        """fixes pickle hiccup b/c of __getattr__ override"""
        self.__dict__.update(state)

    def __repr__(self):
        if self.name:
            return self.name
        else:
            return ' '.join((self.__class__.__name__, self.id))

    def __str__(self):
        return self.__repr__()

    def __getattr__(self, attr):
        """
        Monkey patch of the year, 2014.
        """
        if attr not in self.__dict__:
            return None

    def _delete_extra(self):
        """
        Second runner up.
        """
        significant_false_vals = False, 0
        delete_these = [attr for attr, val in self.__dict__.items()
                        if not val and val not in significant_false_vals]

        for attr in delete_these:
            delattr(self, attr)

    def _dynamic_attr(self):
        """
        Consolation prize.
        """
        for name, attr in self._properties.items():
            setattr(self, name, attr)

        del self._properties

    def _fetch(self, url=None):
        if not url:
          url = self.url

        response = self.session.get(url)

        if not response.ok:
            raise Exception(("There was an error with your request ",
                            url, response.status_code, response.reason))

        self._content = BeautifulSoup(response.text)

    def read(self, pg=1):
        if self.unread:
            self.unread = False


class SAListObj(SAObj):
    def __init__(self, *args, collection=None, **properties):
        self.page = None
        self.pages = None
        self.navi = None

        self._collection = collection
        self.children = self._collection
        super(SAListObj, self).__init__(*args, **properties)

    def _setup_navi(self):
        if not self.navi:
            navi = self._content.find('div', 'pages')
            self.navi = SAPageNavi(self, content=navi)

    def read(self, pg=1):
        super(SAListObj, self).read(pg)

        url = self.url + '&pagenumber=' + str(pg)
        self._fetch(url)
        self._setup_navi()
        self.navi.read(pg)


class SAPageNavi(SAObj):
    def __init__(self, *args, **properties):
        super(SAPageNavi, self).__init__(*args, **properties)

        self.page = 1
        self.pages = 1

    def read(self, pg=1):
        super(SAPageNavi, self).read(pg)

        self.page = pg
        self._parse_page_selector()
        self._modify_parent()
        self._delete_extra()

    def _modify_parent(self):
        self.parent.page = self.page
        self.parent.pages = self.pages

    def _parse_page_selector(self):
        page_selector = self._content.find_all('option')

        if len(page_selector):
            self.pages = page_selector[-1].text
        else:
            self.pages = 1