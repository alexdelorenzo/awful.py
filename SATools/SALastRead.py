from SATools.SAObj import SAObj
from SATools.SATypes import TriggerProperty

from math import floor


class SALastRead(SAObj):
    url_last_post = TriggerProperty('read', 'url_last_post')
    unread_pages = TriggerProperty('read', 'unread_pages')
    unread_count = TriggerProperty('read', 'unread_count')
    url_switch_off = TriggerProperty('read', 'url_switch_off')

    def __init__(self, parent, id, content, name=None, **properties):
        super(SALastRead, self).__init__(parent, id, content, name, **properties)
        self.page = self.parent.page
        self.pages = self.parent.pages
        self._delete_extra()

    def __repr__(self):
        unread_posts = str(self.unread_count) + ' unread posts'
        pages_count = self.unread_pages + 1 if self.unread_count else 0
        unread_pages = str(pages_count) + ' unread pages'
        return ' '.join((unread_posts, 'in', unread_pages))

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

    def read(self, pg=1):
        super(SALastRead, self).read(pg)
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