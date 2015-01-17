from sa_tools.parsers.tools.regex_manager import RegexManager
from sa_tools.parsers.parser import Parser
from sa_tools.parsers.tools.wrapper import BeauToLxml

from collections import OrderedDict
from math import ceil


class ThreadParser(Parser, RegexManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, content: BeauToLxml=None) -> (iter, iter):
        content = self.wrap(content, wrapper=BeauToLxml)
        self._delete_extra()

        if content:
            info_gen = self.gen_info(content)

        else:
            info_gen = self._parse_from_url()

        post_gen = gen_posts(content)

        return info_gen, post_gen

    def gen_posts(self, content: BeauToLxml or str or bytes):
        content = self.wrap(content, wrapper=BeauToLxml)

        return gen_posts(content)

    def set_parser_map(self, parser_map: dict=None) -> None:
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

        super().set_parser_map(parser_map)

    def set_regex_strs(self, regex_strs: dict=None) -> None:
        dicts = dict, OrderedDict
        is_dict = isinstance(regex_strs, dicts)

        if not is_dict:
            regex_strs = \
                {'lastpost': "([0-9]+:[0-9]+) ([A-Za-z 0-9]*, 20[0-9]{2})(.*)",
                 'rating': "([0-9]*) votes - ([0-5][\.[0-9]*]?) average"}

        super().set_regex_strs(regex_strs)

    def _parse_from_url(self, content: BeauToLxml) -> (str, str):
        yield parse_first_post(content)
        yield 'title', content.find('a', 'bclast').text.strip()

    def gen_info(self, content: BeauToLxml=None) -> iter(((str, str),)):
        content = self.wrap(content, wrapper=BeauToLxml)
        needs_regex = 'rating', 'lastpost'
        tds = content.find_all('td')

        for td in tds:
            td_class = td['class']

            if isinstance(td_class, list):
                td_class = td_class[-1]

            text = td.text.strip()

            if td_class in needs_regex:
                info_pair = self.dispatch(td_class, text, td, self.regex_matches)

            else:
                info_pair = self.dispatch(td_class, text, td)

            if info_pair:
                yield info_pair

                if td_class == 'replies':
                    yield parse_page_count(text)

                elif td_class == 'title':
                    yield 'name', info_pair[-1]

        yield parse_last_seen(content)


def expand(func):
    def new(arg):
        return func(*arg)
    return new


def gen_posts(content: BeauToLxml) -> iter((str, BeauToLxml)):
    posts_content = content.find_all('table', 'post')

    for post in posts_content:
        yield post['id'][4:], post


def parse_first_post(content: BeauToLxml) -> (str, (str, BeauToLxml, bool)):
    post_content = content.find('table', 'post')

    post_id = post_content['id'][4:]
    result = post_id, post_content, True

    return 'op', result


def parse_icon(key: str, val: str, content: BeauToLxml) -> (str, str):
    text = content.a['href'].split('posticon=')[-1]

    return key, text


def parse_last_post(key: str, val: str, content: BeauToLxml, regex_matches) -> (str, dict):
    #TODO: use the groups() method
    groups = 'time', 'date', 'user'
    matches = regex_matches(key, val)
    matches = dict(zip(groups, matches))

    return key, matches


def parse_author(key: str, val, content: BeauToLxml) -> (str, (str, str)):
    link = content.a
    author = link.text.strip()
    user_id = link['href'].split('id=')[-1]
    result = user_id, author

    return key, result


def parse_page_count(val: str) -> (str, int):
    pages = ceil(int(val) / 40.0)
    key = 'pages'

    return key, pages


def parse_last_seen(content: BeauToLxml) -> (str, BeauToLxml):
    last_read = content.find('div', 'lastseen')
    key = 'last_read'

    return key, last_read


def parse_title(key: str, val, content: BeauToLxml) -> (str, str):
    text = content.find('a', 'thread_title').text
    key = 'title'

    return key, text


def parse_rating(key: str, val, content: BeauToLxml, regex_matches) -> (str, dict):
    img_tag = content.img

    if img_tag:
        title_attr = img_tag['title'].strip()

        votes, avg = regex_matches(key, title_attr)
        votes, avg = int(votes), float(avg)
        stars = round(avg)

        rating = {'votes': votes,
                  'avg': avg,
                  'stars': stars}

    else:
        rating = {}

    return key, rating


def parse_views(key: str, val, content: BeauToLxml) -> (str, int):
    views = int(content.text.strip())

    return key, views


def parse_replies(key: str, val, content: BeauToLxml) -> (str, int):
    reply_count = int(content.text.strip())

    return key, reply_count