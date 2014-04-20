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
            self.content = BeautifulSoup(self.content)

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
        self.wrap_parent_content()


class SAParser(SAObj):
    def __init__(self, parent, wrapper=BSWrapper, parser_map=None, *args, **kwargs):
        super(SAParser, self).__init__(parent, *args, **kwargs)
        self.id = self.parent.id
        self.wrapper = None
        self._parser_map = None

        self.set_wrapper(wrapper)
        self.set_parser_map(parser_map)
        self._delete_extra()

    def set_wrapper(self, wrapper=BSWrapper):
        self.wrapper = BSWrapper(self.parent)

        if self.parent._content:
            self.wrapper.wrap_parent_content()

    def set_parser_map(self, parser_map=None):
        if parser_map is None:
            parser_map = dict()

        self._parser_map = parser_map

    def dispatch(self, key, val=None, content=None):
        if key not in self._parser_map:
            return

        self._parser_map[key](key, val, content)

    def parse(self):
        self.read()
        self.wrapper.wrap_parent_content()

    @property
    def content(self):
        return self.wrapper.content

    @content.setter
    def content(self, new_val):
        self.wrapper.content = new_val


class SANaviParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SANaviParser, self).__init__(*args, **kwargs)

    def parse(self):
        super(SANaviParser, self).parse()

    @staticmethod
    def parse_navi(parent):
        wrapper = BSWrapper(parent)
        navi_content = wrapper.content.find('div', 'pages')
        return navi_content


class SAPageNaviParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SAPageNaviParser, self).__init__(*args, **kwargs)

    def parse(self):
        super(SAPageNaviParser, self).parse()
        self._parse_page_selector()

    def _parse_page_selector(self):
        page_selector = self.content.find_all('option')

        if len(page_selector):
            self.parent.pages = page_selector[-1].text
        else:
            self.parent.pages = 1


class SAForumParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SAForumParser, self).__init__(*args, **kwargs)

    def parse(self):
        super(SAForumParser, self).parse()
        if self.parent._index:
            return

        self.get_subforums()
        self.get_threads()

    def get_subforums(self):
        if not self.has_subforums():
            return

        if self.children:
            for subforum in self.children:
                _id = subforum.id
                self.parent.subforums[_id] = subforum

        else:
            content = self.content
            tr_subforums = content.find_all('tr', 'subforum')

            for tr_subforum in tr_subforums:
                href = tr_subforum.a['href']
                subforum_id = href.split("forumid=")[-1]
                name = tr_subforum.a.text

                self.parent._add_subforum(subforum_id, name)

    def has_subforums(self):
        content = self.content

        if content.table:
            return content.table['id'] == 'subforums'
        else:
            return False

    def get_threads(self):
        if self.unread:
            self.parse()

        self.content = self.content.find('div', id='content')
        thread_blocks = self.content.find_all('tr', 'thread', id=True)

        for tr_thread in thread_blocks:
            thread_id = IntOrNone.int_check(tr_thread['id'][6:])
            self.parent._add_thread(thread_id, tr_thread)


class SAThreadParser(SAParser):
    def __init__(self, parent, *args, **kwargs):
        super(SAThreadParser, self).__init__(parent, *args, **kwargs)
        self._regexes = dict()

        self.set_parser_map()
        self._dynamic_attr()

    def parse(self):
        super(SAThreadParser, self).parse()
        self.parse_info()
        self.parse_posts()
        self._delete_extra()

    def parse_info(self):
        self._parse_tr_thread()

    def parse_posts(self):
        posts_content = self.content.find_all('table', 'post')

        for post in posts_content:
            post_id = post['id'][4:]
            self.parent._add_post(post_id, post)

    def set_parser_map(self, parser_map=None):
        if not parser_map:
            parser_map = \
                {'icon': self._parse_icon,
                 'lastpost': self._parse_lastpost,
                 'replies': self._parse_replies,
                 'author': self._parse_author,
                 'title': self._parse_title,
                 'title_sticky': self._parse_title,
                  'views': self._parse_views,
                  'rating': self._parse_rating}

        super(SAThreadParser, self).set_parser_map(parser_map)

    def _parse_tr_thread(self):
        if not self.content:
            return

        for td in self.content.find_all('td'):
            td_class = td['class'][-1]
            text = td.text.strip()

            self.dispatch(td_class, text, td)

    def _parse_icon(self, key, val, content):
        text = content.a['href'].split('posticon=').pop(-1)
        setattr(self.parent, key, text)

    def _parse_lastpost(self, key, val, content):
        groups = 'time', 'date', 'user'

        if key in self._regexes:
            regex_c = self._regexes[key]
        else:
            regex = "([0-9]+:[0-9]+) ([A-Za-z 0-9]*, 20[0-9]{2})(.*)"
            regex_c = compile(regex)
            self._regexes[key] = regex_c

        matches = regex_c.search(val).groups()
        matches = dict(zip(groups, matches))
        setattr(self.parent, key, matches)

    def _parse_author(self, key, val, content):
        link = content.a
        author = link.text.strip()
        user_id = link['href'].split('id=')[-1]
        self.parent._add_author(user_id, author)

    def _parse_replies(self, key, val, content):
        self._parse_pagecount(val)
        link = content.a

        if link:
            replies_url = self.base_url + link['href']
            replies_count = int(content.a.text.strip())
            replies = {'url': replies_url,
                       'count': replies_count}
            setattr(self.parent, key, replies)

    def _parse_views(self, key, val, content):
        views = int(content.text.strip())
        setattr(self.parent, key, views)

    def _parse_rating(self, key, val, content):
        img_tag = content.img

        if img_tag:
            title_attr = img_tag['title'].strip()
            votes_index = title_attr.index(' votes')
            votes = int(title_attr[:votes_index])

            avg_index = title_attr.index(' average')
            dash_index = title_attr.index('- ') + 2
            avg = float(title_attr[dash_index:avg_index])

            stars = img_tag['src'].split('/').pop(-1).split('stars').pop(0)
            stars = int(stars)

            rating = {'votes': votes,
                      'avg': avg,
                      'stars': stars}
            setattr(self.parent, key, rating)

    def _parse_title(self, key, val, content):
        text = content.find('a', 'thread_title').text
        key = 'title'

        self._parse_lastseen(content)
        setattr(self.parent, key, text)

    def _parse_lastseen(self, content):
        last_read = content.find('div', 'lastseen')
        self.parent._add_last_read(last_read)

    def _parse_pagecount(self, val):
        pages = ceil(int(val) / 40.0)
        key = 'pages'
        setattr(self.parent, key, pages)





