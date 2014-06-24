from sa_tools.parsers.parser import Parser

from math import floor


class LastReadParser(Parser):
    def __init__(self, *args, **kwargs):
        super(LastReadParser, self).__init__(*args, **kwargs)

    def parse(self):
        super(LastReadParser, self).parse()
        self._parse_unread()

    def _parse_unread(self):
        close_link = self.content.a
        stop_tracking_url = self.parent._base_url + close_link['href']
        last_post_link = self.content.find('a', 'count')
        self.parent.url_switch_off = stop_tracking_url

        if last_post_link:
            unread_count = int(last_post_link.text)
            last_post_url = self.parent._base_url + last_post_link['href']
            self.parent.url_last_post = last_post_url
            self.parent.unread_count = unread_count
            self.parent.unread_pages = int(floor(unread_count / 40.0))