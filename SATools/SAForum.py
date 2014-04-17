from SATools.SAThread import SAThread
from SATools.SAObj import SAListObj
from SATools.SATypes import TriggerProperty as TrigProp

from collections import OrderedDict as ordered


class SAForum(SAListObj):
    threads = TrigProp(trigger='read', name='threads')

    def __init__(self, parent, id, content=None, name=None,
                 page=1, subforums=None, **properties):
        super(SAForum, self).__init__(parent, id, content, name, page=page, **properties)
        self.subforums = subforums
        self.base_url = \
            'http://forums.somethingawful.com/forumdisplay.php'
        self.url = self.base_url + '?forumid=' + str(id)
        self.threads = ordered()

    def read(self, pg=1):
        super(SAForum, self).read(pg)
        self.threads = self._get_threads(pg)

        if not self.subforums and self._has_subforums():
            self.subforums = ordered(self._gen_subforums())

        self._delete_extra()

    def _has_subforums(self):
        if self._content.table:
            return self._content.table['id'] == 'subforums'
        else:
            return False

    def _gen_subforums(self):
        for tr_subforum in self._content.find_all('tr', 'subforum'):
            subforum_id = tr_subforum.a['href'].split("forumid=")[-1]
            name = tr_subforum.a.text

            forum_obj = SAForum(self, subforum_id, name)

            yield forum_obj.id, forum_obj

    def _get_threads(self, pg):
        self._content = self._content.find('div', id='content')
        threads = ordered(self._gen_threads())

        return threads

    def _gen_threads(self):
        thread_blocks = self._content.find_all('tr', 'thread', id=True)

        for tr_thread in thread_blocks:
            thread_id = tr_thread['id'][6:]
            val = self._thread_obj_persist(thread_id, tr_thread)

            yield val.id, val

    def _thread_obj_persist(self, thread_id, tr_thread):
        if thread_id in self.threads:
            val = self.threads[thread_id]
            val._content = tr_thread
            val._parse_tr_thread()

        else:
            val = SAThread(self, thread_id, tr_thread)

        return val