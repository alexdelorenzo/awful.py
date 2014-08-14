from sa_tools.parsers.parser import Parser

from math import floor


class LastReadParser(Parser):
    def __init__(self, *args, **kwargs):
        super(LastReadParser, self).__init__(*args, **kwargs)

    def parse(self):
        super(LastReadParser, self).parse()

        pairs = gen_parent_changes(self.content, self.parent._base_url)

        for name, attr in pairs:
            setattr(self, name, attr)



def gen_parent_changes(content, url):
    close_link = content.a
    stop_tracking_url = url + close_link['href']
    last_post_link = content.find('a', 'count')

    yield 'url_switch_off', stop_tracking_url

    if last_post_link:
        unread_count = int(last_post_link.text)
        last_post_url = url + last_post_link['href']

        yield 'url_last_post', last_post_url
        yield 'unread_count', unread_count
        yield 'unread_pages', int(floor(unread_count / 40.0))