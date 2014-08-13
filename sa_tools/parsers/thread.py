from sa_tools.parsers.tools.regex_manager import RegexManager
from sa_tools.parsers.parser import Parser

from collections import OrderedDict as ordered
from math import ceil


class ThreadParser(Parser, RegexManager):
    def __init__(self, parent, *args, **kwargs):
        super(ThreadParser, self).__init__(parent, *args, **kwargs)
        self._dynamic_attr()

    def parse(self):
        super(ThreadParser, self).parse()
        self._delete_extra()
        info_gen = self.parse_info()
        post_gen = gen_posts(self.content)

        return info_gen, post_gen

    def parse_info(self):
        if self.content:
            return self.gen_info()

        else:
            return self._parse_from_url()

    def set_parser_map(self, parser_map=None):
        if not parser_map:
            parser_map = \
                {'icon': parse_icon,
                 'lastpost': parse_last_post,
                 'replies': parse_replies,
                 'author': parse_author,
                 'title': parse_title,
                 'title_sticky': parse_title,
                 'views': parse_views,
                 'rating': parse_rating}

        super(ThreadParser, self).set_parser_map(parser_map)

    def set_regex_strs(self, regex_strs=None):
        dicts = dict, ordered
        is_dict = isinstance(regex_strs, dicts)

        if not is_dict:
            lastpost, rating = \
                "([0-9]+:[0-9]+) ([A-Za-z 0-9]*, 20[0-9]{2})(.*)", \
                "([0-9]*) votes - ([0-5][\.[0-9]*]?) average"

            regex_strs = \
                {'lastpost': lastpost,
                 'rating': rating}

        super(ThreadParser, self).set_regex_strs(regex_strs)

    def _parse_from_url(self):
        #self.parent.read()
        yield parse_first_post(self.content)
        yield 'title', self.content.find('a', 'bclast').text.strip()

    def gen_info(self, content=None):
        if not self.content:
            return

        need_regex = 'rating', 'lastpost'
        tds = self.content.find_all('td')

        for td in tds:
            td_class = td['class'][-1]
            text = td.text.strip()

            if td_class in need_regex:
                pair = self.dispatch(td_class, text, td, self.regex_matches)

            else:
                pair = self.dispatch(td_class, text, td)

            if pair:
                yield pair

                if td_class == 'replies':
                    yield parse_page_count(text)

                elif td_class == 'title':
                    yield 'name', pair[-1]


def gen_posts(content):
    posts_content = content.find_all('table', 'post')
    post_gen = ((post['id'][4:], post) for post in posts_content)

    return post_gen


def parse_first_post(content):
    post_content = content.find('table', 'post')

    post_id = post_content['id'][4:]
    result = post_id, post_content, True

    return 'op', result


def parse_icon(key, val, content):
    text = content.a['href'].split('posticon=')[-1]

    return key, text


def parse_last_post(key, val, content, regex_matches):
    groups = 'time', 'date', 'user'
    matches = regex_matches(key, val)
    matches = dict(zip(groups, matches))

    return key, matches


def parse_author(key, val, content):
    link = content.a
    author = link.text.strip()
    user_id = link['href'].split('id=')[-1]
    result = user_id, author

    return key, result


def parse_page_count(val):
    pages = ceil(int(val) / 40.0)
    key = 'pages'

    return key, pages


def parse_last_seen(content):
    last_read = content.find('div', 'lastseen')
    key = 'last_read'

    return key, last_read


def parse_title(key, val, content):
    text = content.find('a', 'thread_title').text
    key = 'title'

    return key, text


def parse_rating(key, val, content, regex_matches):
    img_tag = content.img

    if img_tag:
        title_attr = img_tag['title'].strip()

        votes, avg = regex_matches(key, title_attr)
        votes = int(votes)
        avg = float(avg)
        stars = round(avg)

        rating = {'votes': votes,
                  'avg': avg,
                  'stars': stars}

    else:
        rating = {}

    return key, rating


def parse_views(key, val, content):
    views = int(content.text.strip())

    return key, views


def parse_replies(key, val, content):
    parse_page_count(val)
    reply_count = int(content.text.strip())

    return  key, reply_count