from SATools.SAObj import SAObj
from bs4 import BeautifulSoup

class SAPoster(SAObj):
    def __init__(self, parent, id=None, content=None, name=None, **properties):
        super(SAPoster, self).__init__(parent, id, content, name=name, **properties)
        self.avatar_url = None
        self.title = None
        self.reg_date = None

        self.post_count = None
        self.post_rate = None
        self.last_post = None
        self.contact_info = dict({})

        if self.id:
            self.url = "https://forums.somethingawful.com/member.php?action=getinfo&userid=" + self.id

    def read(self):
        super(SAPoster, self).read()
        if self._content:
            self._parse_tr()
        else:
            self._get_profile_from_url()

        self._delete_extra()


    def _get_profile_from_url(self):
        response = self.session.get(self.url)
        bs_content = BeautifulSoup(response.text)
        table = bs_content.find('table', _class='standard')
        rows = table.find_all('tr')
        pertinent_info = rows[1]

        self._content = pertinent_info
        self.read()

    def _parse_tr(self):
        if not self.id:
            self.id = self._content.td['class'].pop()
        if self._content.img:
            self.avatar_url = self._content.img['src']
        if not self.name:
            self.name = self._content.find('dt', 'author')

        self.title = self._content.find('dd', 'title')
        self.reg_date = self._content.find('dd', 'registered')

        self._parse_contact_info()

    def _parse_contact_info(self):
        bs_contact = self._content.find('dl', _class='contacts')
        dts, dds = bs_contact.find_all('dt'), bs_contact.find_all('dd')
        pairs = {dt['class']: dd.text for dt, dd in zip(dts, dds)}
        self.contact_info = pairs
