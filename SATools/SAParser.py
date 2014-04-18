from SATools.SAObj import SAObj
from SATools.SATypes import TriggerProperty, IntOrNone

from collections import OrderedDict as ordered
from bs4 import BeautifulSoup, element
from math import ceil, floor
from re import compile


class BSWrapper(object):
    def __init__(self, parent, *args, **kwargs):
        super(BSWrapper, self).__init__()
        self.parent = parent
        self._bs_wrappers = BeautifulSoup, element.Tag

    def wrap_parent_content(self):
        if not self._is_wrapped():
            self.content = BeautifulSoup(self.parent._content)

    def _is_wrapped(self, content=None):
        if not content:
            content = self.content

        content_type = type(content)

        if content_type in self._bs_wrappers:
            return True
        else:
            return False

    @property
    def content(self):
        return self.parent._content

    @content.setter
    def content(self, new_val):
        self.parent._content = new_val


class SAParser(SAObj):
    def __init__(self, parent, wrapper=BSWrapper, *args, **kwargs):
        super(SAParser, self).__init__(parent, *args, **kwargs)
        self.set_wrapper(wrapper)
        self._delete_extra()
        self._parser_map = dict()
        self.id = self.parent.id

    def set_wrapper(self, wrapper=BSWrapper):
        self.wrapper = BSWrapper(self.parent)

        if self.parent._content:
            self.wrapper.wrap_parent_content()

    def set_parser_map(self):
        pass

    def dispatch(self, key, val=None, content=None):
        if key not in self._parser_map:
            return

        self._parser_map[key](key, val, content)

    def parse(self):
        self.read()
        self.wrapper.wrap_parent_content()


class SAForumParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SAForumParser, self).__init__(*args, **kwargs)

    def get_subforums(self):
        pass

    def has_subforums(self):
        content = self.wrapper.content

        if content.table:
            return content.table['id'] == 'subforums'
        else:
            return False

    def get_threads(self):
        if self.unread:
            self.parse()

        self.wrapper.content = self.wrapper.content.find('div', id='content')
        thread_blocks = self.wrapper.content.find_all('tr', 'thread', id=True)

        for tr_thread in thread_blocks:
            thread_id = IntOrNone.int_check(tr_thread['id'][6:])
            self.parent._add_thread(thread_id, tr_thread)


class SAThreadParser(SAParser):
    def __init__(self, parent, tr_thread=None, *args, **kwargs):
        super(SAThreadParser, self).__init__(parent, *args, **kwargs)
        self._regex = ""

        self.set_parser_map()
        self._dynamic_attr()

    def parse(self):
        super(SAThreadParser, self).parse()
        self._parse_tr_thread()
        self._delete_extra()

    def set_parser_map(self, parser_map=None):
        super(SAThreadParser, self).set_parser_map()

        if not parser_map:
            parser_map = \
                {'icon': self._parse_icon,
                 'lastpost': self._parse_lastpost,
                 'replies': self._parse_replies,
                 'author': self._parse_author,
                 'title': self._parse_title,
                 'title_sticky': self._parse_title}

        self._parser_map = parser_map

    def _parse_tr_thread(self):
        if not self.wrapper.content:
            return

        for td in self.wrapper.content.find_all('td'):
            td_class = td['class'].pop()
            text = td.text.strip()

            self.dispatch(td_class, text, td)

    def _parse_posts(self):
        posts_content = self.wrapper.content.find_all('table', 'post')

        for post in posts_content:
            post_id = post['id'][4:]
            self.parent._add_post(post_id, post)

    def _parse_icon(self, key, val, content):
        text = content.a['href'].split('posticon=').pop(-1)
        setattr(self.parent, key, text)

    def _parse_lastpost(self, key, val, content):
        groups = 'time', 'date', 'user'

        if not self._regex:
            regex = "([0-9]+:[0-9]+) ([A-Za-z 0-9]*, 20[0-9]{2})(.*)"
            self._regex = compile(regex)

        matches = self._regex.search(val).groups()
        matches = dict(zip(groups, matches))
        setattr(self.parent, key, matches)

    def _parse_replies(self, key, val, content):
        pages = ceil(int(val) / 40.0)
        key = 'pages'
        setattr(self.parent, key, pages)

    def _parse_author(self, key, val, content):
        user_id = content.a['href'].split('id=')[-1]
        key = 'user_id'
        setattr(self.parent, key, user_id)

    def _parse_title(self, key, val, content):
        text = content.find('a', 'thread_title').text
        key = 'title'

        self._parse_lastseen(content)
        setattr(self.parent, key, text)

    def _parse_lastseen(self, content):
        last_read = content.find('div', 'lastseen')
        self.parent._add_last_read(last_read)
