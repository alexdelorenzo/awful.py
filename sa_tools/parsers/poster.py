from sa_tools.parsers.parser import SAParser


class SAProfileParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SAProfileParser, self).__init__(*args, **kwargs)

    def parse(self):
        if self.content:
            super(SAProfileParser, self).parse()
            self._parse_tr()

        else:
            self._get_profile_from_url()
            self._parse_contact_info()

    def _parse_tr(self):
        if not self.parent.id:
            self.parent.id = self.content.td['class'][-1]

        if self.content.img:
            self.parent.avatar_url = self.content.img['src']

        if not self.parent.name:
            self.parent.name = self.content.find('dt', 'author').text.strip()

        self.parent.title = self.content.find('dd', 'title')
        self.parent.reg_date = self.content.find('dd', 'registered').text.strip()

    def _parse_contact_info(self):
        bs_contact = self.content.find('dl', 'contacts')
        dts, dds = bs_contact.find_all('dt'), bs_contact.find_all('dd')

        contact_info = dict()
        bad_vals = 'pm', 'not set'

        for dt, dd in zip(dts, dds):
            service = dt['class'][-1]
            handle = dd.text.strip()

            good_service = service not in bad_vals
            good_handle = handle not in bad_vals
            good_pair = good_service and good_handle

            if good_pair:
                contact_info[service] = handle

        self.parent.contact_info = contact_info

    def _get_profile_from_url(self):
        self.parent._fetch()
        table = self.content.find('table', 'standard')
        rows = table.find_all('tr')
        pertinent_info = rows[1]

        self.content = pertinent_info
        self.parent.read()