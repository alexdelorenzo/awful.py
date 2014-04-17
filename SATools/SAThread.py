from SATools.SAPost import SAPost
from SATools.SAObj import SAObj, SAListObj
from SATools.SATypes import TriggerProperty as TrigProp

from collections import OrderedDict as ordered
from math import ceil, floor
from re import compile


class SAThread(SAListObj):
    posts = TrigProp(name='posts', trigger='read')

    def __init__(self, parent, id, tr_thread=None, **properties):
        super(SAThread, self).__init__(parent, id, content=tr_thread, page=1, **properties)
        self.base_url = "http://forums.somethingawful.com/"
        self.url = self.base_url + '/showthread.php?threadid=' + str(self.id)
        self._parser_map = None
        self._regex = None

        self._set_parser_map()
        self._parse_tr_thread()
        self._dynamic_attr()
        self.name = self.title

    def _set_parser_map(self):
        dispatch = \
            {'icon': self._parse_icon,
             'lastpost': self._parse_lastpost,
             'replies': self._parse_replies,
             'author': self._parse_author,
             'title': self._parse_title,
             'title_sticky': self._parse_title}

        self._parser_map = dispatch

    def _parse_tr_thread(self):
        if not self._content:
            return

        for td in self._content.find_all('td'):
            td_class = td['class'].pop()
            text = td.text.strip()
            self._parsing_dispatch(td_class, text, td)

        #self._dynamic_attr()

    def _get_posts(self):
        posts = ordered(self._parse_posts())
        return posts

    def _parse_posts(self):
        for post in self._content.find_all('table', 'post'):
            post_id = post['id'][4:]
            sa_post = SAPost(self, post_id, post)

            yield sa_post.id, sa_post

    def _parsing_dispatch(self, key, val, content):
        if key not in self._parser_map:
            return

        self._parser_map[key](key, val, content)

    def _parse_icon(self, key, val, content):
        text = content.a['href'].split('posticon=').pop(-1)
        setattr(self, key, text)

    def _parse_lastpost(self, key, val, content):
        groups = 'time', 'date', 'user'

        if not self._regex:
            regex = "([0-9]+:[0-9]+) ([A-Za-z 0-9]*, 20[0-9]{2})(.*)"
            self._regex = compile(regex)

        matches = self._regex.search(val).groups()
        matches = dict(zip(groups, matches))
        setattr(self, key, matches)

    def _parse_replies(self, key, val, content):
        pages = ceil(int(val) / 40.0)
        key = 'pages'
        setattr(self, key, pages)

    def _parse_author(self, key, val, content):
        user_id = content.a['href'].split('id=')[-1]
        key = 'user_id'
        setattr(self, key, user_id)

    def _parse_title(self, key, val, content):
        text = content.find('a', 'thread_title').text
        key = 'title'
        last_read = content.find('div', 'lastseen')
        last_read = self._parse_lastseen(key, val, last_read)

        setattr(self, 'last_read', last_read)
        setattr(self, key, text)

    def _parse_lastseen(self, key, val, content):
        return SALastRead(self, self.id, content) if content else None

    def read(self, page=1):
        super(SAThread, self).read(page)
        self.posts = self._get_posts()
        self._delete_extra()


class SALastRead(SAObj):
    url_last_post = TrigProp(name='url_last_post', trigger='read')
    unread_read_pages = TrigProp(name='unread_pages', trigger='read')
    unread_count = TrigProp(name='unread_count', trigger='read')
    url_switch_off = TrigProp(name='url_switch_off', trigger='read')

    def __init__(self, parent, id, content, name=None, **properties):
        super(SALastRead, self).__init__(parent, id, content, name, **properties)
        self.page = self.parent.page
        self.pages = self.parent.pages

    def _parse_unread(self):
        close_link = self._content.a
        stop_tracking_url = self.parent.base_url + close_link['href']
        last_post_link = self._content.find('a', 'count')
        self.url_switch_off = stop_tracking_url

        if last_post_link:
            unread_count = int(last_post_link.text)
            last_post_url = self.parent.base_url + last_post_link['href']
            self.url_last_post = last_post_url
            self.unread_count = unread_count
            self.unread_pages = int(floor(unread_count / 40.0))

    def read(self):
        super(SALastRead, self).read()
        self.page = self.parent.page
        self.pages = self.parent.pages
        self._parse_unread()
        self._delete_extra()

    def jump_to_new(self):
        if self.parent.pages and self.unread_pages:
            unread_page = self.parent.pages - self.unread_pages
            self.parent.read(unread_page)

    def stop_tracking(self):
        self.session.post(self.url_switch_off)