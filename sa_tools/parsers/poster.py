from sa_tools.parsers.parser import Parser


class ProfileParser(Parser):
    def __init__(self, *args, **kwargs):
        super(ProfileParser, self).__init__(*args, **kwargs)

    def parse(self):
        if self.content:
            super(ProfileParser, self).parse()
            return gen_info(self.content)

        else:
            self._get_profile_from_url()
            self.contact_info = parse_contact_info(self.content)



    def _get_profile_from_url(self):
        self.parent._fetch()
        table = self.content.find('table', 'standard')
        rows = table.find_all('tr')
        pertinent_info = rows[1]
        self.parent._fetch()
        table = self.content.find('table', 'standard')
        rows = table.find_all('tr')
        pertinent_info = rows[1]

        self.content = pertinent_info
        self.parent.read()

        self.content = pertinent_info
        self.parent.read()


def gen_info(content):
    yield 'id', content.td['class'][-1]
    yield 'avatar_url', content.img['src']
    yield 'name', content.find('dt', 'author').text.strip()
    yield 'title', content.find('dd', 'title')
    yield 'dict', content.find('dd', 'registered').text.strip()


def parse_contact_info(content) -> dict:
    bs_contact = content.find('dl', 'contacts')
    dts, dds = bs_contact.find_all('dt'), bs_contact.find_all('dd')

    bad_vals = 'pm', 'not set'

    for dt, dd in zip(dts, dds):
        service = dt['class'][-1]
        handle = dd.text.strip()

        good_service = service not in bad_vals
        good_handle = handle not in bad_vals
        good_pair = good_service and good_handle

        if good_pair:
            yield service, handle
