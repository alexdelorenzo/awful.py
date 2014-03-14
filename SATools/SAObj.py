from bs4 import BeautifulSoup


class SAObj(object):
    """
    The gloves are off. It's a fucking free for all.
    """
    def __init__(self, id=None, session=None, content=None, parent=None,
                 name=None, url=None, **properties):
        super(SAObj, self).__init__()
        self.content = content
        self.session = session
        self.id = id
        self.name = name
        self.parent = parent
        self.unread = True
        self.url = url
        self.base_url = ""

        self._properties = properties

    def __repr__(self):
        if self.name:
            return self.name
        else:
            return ' '.join((self.__class__.__name__, self.id))

    def __str__(self):
        return self.__repr__()

    def __getattr__(self, item):
        """
        Monkey patch of the year, 2014.
        """
        if item not in self.__dict__:
            return None

    def _delete_extra(self):
        """
        Second runner up.
        """
        delete = [key for key, val in self.__dict__.items()
                  if not val and val is not 0]
        for attr in delete:
            delattr(self, attr)

    def _dynamic_attr(self):
        """
        Consolation prize.
        """
        for name, attr in self.properties.items():
            setattr(self, name, attr)

    def read(self, pg=1):
        if self.unread:
            self.unread = False


class SAListObj(SAObj):
    def __init__(self, *args, **properties):
        super(SAListObj, self).__init__(*args, **properties)
        self.page = None
        self.pages = None
        self.navi = None
        self.children = None

        self._collection = None
        self._content = None

    def read(self, pg=1):
        super(SAListObj, self).read(pg)

        url = self.url + '&pagenumber=' + str(pg)
        request = self.session.get(url)
        self._content = BeautifulSoup(request.text)

        if not self.navi:
            navi = self._content.find('div', 'pages')
            self.navi = SAPageNav(content=navi, parent=self)

        self.navi.read(pg)



class SAPageNav(SAObj):
    def __init__(self, **properties):
        super(SAPageNav, self).__init__(**properties)
        self.page = 1
        self.pages = 1

    def read(self, pg=1):
        super(SAPageNav, self).read(pg)
        self.page = pg
        page_selector = self.content.find_all('option')
        if len(page_selector):
            self.pages = page_selector[-1].text
        else:
            self.pages = 1

        self._modify_parent()
        self._delete_extra()

    def _modify_parent(self):
        self.parent.page = self.page
        self.parent.pages = self.pages

