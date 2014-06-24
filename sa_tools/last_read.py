from sa_tools.base.sa_obj import SAObj
from sa_tools.base.descriptors import TriggerProperty
from sa_tools.parsers.last_read import LastReadParser


class LastRead(SAObj):
    url_last_post = TriggerProperty('read', 'url_last_post')
    url_switch_off = TriggerProperty('read', 'url_switch_off')

    unread_pages = TriggerProperty('read', 'unread_pages')
    unread_count = TriggerProperty('read', 'unread_count')

    def __init__(self, parent, id, content, name=None, **properties):
        super(LastRead, self).__init__(parent, id, content, name, **properties)
        self.page = self.parent.page
        self.pages = self.parent.pages
        self.unread_count = 0
        self.unread_pages = 0
        self.parser = LastReadParser(self)
        self._base_url = self.parent._base_url

        self._delete_extra()

    def __repr__(self):
        unread_posts = str(self.unread_count) + ' unread posts'
        pages_count = self.unread_pages + 1 if self.unread_count else 0
        unread_pages = str(pages_count) + ' unread pages'
        return ' '.join((unread_posts, 'in', unread_pages))

    def read(self, pg=1):
        super(LastRead, self).read(pg)
        self.page = self.parent.page
        self.pages = self.parent.pages
        self.parser.parse()
        self._delete_extra()

    def jump_to_new(self):
        if self.parent.pages and self.unread_pages:
            unread_page = self.parent.pages - self.unread_pages
            self.parent.read(unread_page)

    def stop_tracking(self):
        self.session.post(self.url_switch_off)