from SATools.SAThread import SAThread
from SATools.SAObj import SAListObj

from collections import OrderedDict as ordered
from math import ceil
import bs4
import re


class SAForum(SAListObj):
    def __init__(self, parent, id, content=None, name=None,
                 page=1, subforums=None, **properties):
        super(SAForum, self).__init__(parent, id, content, name, page=page, **properties)
        self.subforums = subforums
        self.listings = None
        self.base_url = \
            'http://forums.somethingawful.com/forumdisplay.php'
        self.url = self.base_url + '?forumid=' + str(id)
        self.threads = {}

    def read(self, pg=1):
        super(SAForum, self).read(pg)
        self.threads = self._get_threads(pg)
        self.listings = {threadid: thread.title
                         for threadid, thread in self.threads.items()}

        if not self.subforums and self._has_subforums():
            self.subforums = ordered(self._get_subforums())

        self._delete_extra()

    def _has_subforums(self):
        if self.content.table:
            return self.content.table['id'] == 'subforums'
        else:
            return False

    def _get_subforums(self):
        for tr_subforum in self.content.select('tr.subforum'):
            subforum_id = tr_subforum.a['href'].split("forumid=")[-1]
            name = tr_subforum.a.text

            forum_obj = SAForum(self, subforum_id, name)

            yield subforum_id, forum_obj


    def _get_threads(self, pg):
        response = self.session.post(self.base_url,
                                {'forumid': self.id,
                                 'pagenumber': pg})

        self.content = bs4.BeautifulSoup(response.content)
        self.content = self.content.find('div', id='content')
        threads = ordered(self._gen_threads())

        self.page = pg

        return threads

    def _gen_threads(self):
        thread_blocks = self.content.select('tr.thread')

        for tr_thread in thread_blocks:
            thread_id = tr_thread['id'][6:]

            if thread_id in self.threads:
                val = self.threads[thread_id]
            else:
                val = SAThread(self, thread_id, tr_thread)

            key = thread_id
            yield key, val