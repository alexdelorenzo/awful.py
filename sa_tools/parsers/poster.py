from sa_tools.parsers.parser import Parser

from bs4 import Tag


class ProfileParser(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, content: Tag=None):
        if content:
            content = super().parse(content)

            info_gen = gen_info(content)
            contact_info_gen = parse_contact_info(content)

            return info_gen, contact_info_gen

    def _get_profile_from_url(self, content):
        table = content.find('table', 'standard')
        rows = table.find_all('tr')
        pertinent_info = rows[1]

        return self.parse(pertinent_info)


def gen_info(content: Tag) -> (str, str):
    yield 'id', content.td['class'][-1]
    yield 'avatar_url', content.img['src']
    yield 'name', content.find('dt', 'author').text.strip()
    yield 'title', content.find('dd', 'title')
    yield 'dict', content.find('dd', 'registered').text.strip()


def parse_contact_info(content: Tag) -> iter:
    contacts = content.find('dl', 'contacts')
    dts, dds = contacts.find_all('dt'), contacts.find_all('dd')

    bad_vals = 'pm', 'not set'

    for dt, dd in zip(dts, dds):
        service = dt['class'][-1]
        handle = dd.text.strip()

        good_service = service not in bad_vals
        good_handle = handle not in bad_vals
        good_pair = good_service and good_handle

        if good_pair:
            yield service, handle
