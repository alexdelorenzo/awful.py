from bs4 import BeautifulSoup

from SATools.SAObjs.SADynamic import SADynamic
from SATools.SAObjs.SAMagic import SAMagic
from SATools.SAObjs.SADescriptors import IntOrNone


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


