from SATools.SAPost import SAPost
from SATools.SAPoster import SAPoster
from SATools.SAObj import SAObj, SAListObj

from collections import OrderedDict as ordered
from bs4 import BeautifulSoup
from math import ceil, floor
import re


class SAThread(SAListObj):
    def __init__(self, parent, tr_thread=None, **properties):
        super(SAThread, self).__init__(parent, tr_thread=tr_thread, **properties)
        self.base_url = "http://forums.somethingawful.com/"
        self.url = self.base_url + '/showthread.php?threadid=' + self.id
        self.content = None
        self.posts = None
        self.pages = None
        self.page = 1

        self.last_read = None

        self._set_properties(self._parse_tr_thread(tr_thread))
        self._set_properties(properties)

    def __str__(self):
        return self.name

    def read(self, page=1):
        super(SAThread, self).read(page)
        self.content = self._content
        self.posts = self._get_posts()
        self._delete_extra()

    def _set_properties(self, properties):
        for name, attr in properties.items():
            if name == 'user_id':
                name = 'poster'
                attr = SAPoster(self, attr, properties['author'])

            setattr(self, name, attr)

        self.name = self.title

    def _get_posts(self):
        posts = ordered(self._parse_posts())
        return posts

    def _parse_posts(self):
        """TODO: grab more info from content, put it in sa_post module..."""
        for post in self.content.select('table.post'):
            post_id = post['id']
            sa_post = SAPost(self, post_id, post)
            #sa_post.read()
            yield post_id, sa_post

    def _parse_tr_thread(self, tr_thread):
        properties = dict()

        for td in tr_thread.find_all('td'):
            td_class = td['class'].pop()
            text = td.text.strip()

            if td_class == 'icon':
                text = td.a['href'].split('posticon=').pop(-1)

            elif td_class == 'lastpost':
                groups = 'time', 'date', 'user'
                regex = "([0-9]+:[0-9]+) ([A-Za-z 0-9]*, 20[0-9]{2})(.*)"
                matches = re.compile(regex).search(text).groups()
                matches = dict(zip(groups, matches))

                text = matches

            elif td_class == 'replies':
                properties['pages'] = ceil(int(text) / 40)

            elif td_class == 'author':
                user_id = td.a['href'].split('id=')[-1]
                properties['user_id'] = user_id

            elif td_class == 'title' or td_class == 'title_sticky':
                text = td.find('a', 'thread_title').text
                properties['title'] = text

                last_read = td.find('div', 'lastseen')
                if last_read:
                    self.last_read = SALastRead(self.id, self.session, last_read, self)

            properties[td_class] = text

        return properties

class SALastRead(SAObj):
    def __init__(self, parent, id, content, name=None, **properties):
        super(SALastRead, self).__init__(parent, id, content, name, **properties)
        self.page = None
        self.pages = None
        self.url_last_post = None
        self.unread_pages = None
        self.unread_count = None
        self.url_switch_off = None

    def _parse_unread(self):
        close_link = self.content.a
        stop_tracking_url = self.parent.base_url + close_link['href']
        last_post_link = self.content.find('a', 'count')
        self.url_switch_off = stop_tracking_url

        if last_post_link:
            unread_count = last_post_link.text
            last_post_url = self.parent.base_url + last_post_link['href']
            self.url_last_post = last_post_url
            self.unread_count = unread_count
            self.unread_pages = floor(int(unread_count) / 40)


    def read(self):
        super(SALastRead, self).read()
        self._parse_unread()
        self._delete_extra()

    def jump_to_new(self):
        if self.parent.pages and self.unread_pages:
            self.parent.read(self.parent.pages - self.unread_pages)

    def stop_tracking(self):
        self.session.post(self.url_switch_off)




