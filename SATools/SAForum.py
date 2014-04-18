from SATools.SAThread import SAThread
from SATools.SAObj import SAListObj
from SATools.SATypes import TriggerProperty, IntOrNone
from SATools.SAParser import SAForumParser

from collections import OrderedDict as ordered


class SAForum(SAListObj):
    threads = TriggerProperty(trigger='read', name='threads')

    def __init__(self, parent, id, content=None, name=None,
                 page=1, subforums=None, **properties):
        super(SAForum, self).__init__(parent, id, content, name, page=page, **properties)
        print(parent, id, content, name, page, subforums)
        self.subforums = subforums
        self.base_url = \
            'http://forums.somethingawful.com/forumdisplay.php'
        self.url = self.base_url + '?forumid=' + str(id)
        self.threads = ordered()
        self.parser = SAForumParser(self)
        self._index = self._is_index()

    def read(self, pg=1):
        super(SAForum, self).read(pg)
        print(self._index)
        if self._index:
            return

        self.parser.get_threads()

        if not self.subforums and self._has_subforums():
            self.subforums = ordered(self._gen_subforums())

        self._delete_extra()

    def _is_index(self):
        index_ids = None, -1
        return self.id in index_ids

    def _has_subforums(self):
        if self._content.table:
            return self._content.table['id'] == 'subforums'
        else:
            return False

    def _add_thread(self, thread_id, thread_content):
        sa_thread = self._thread_obj_persist(thread_id, thread_content)
        self.threads[sa_thread.id] = sa_thread

    def _gen_subforums(self):
        for tr_subforum in self._content.find_all('tr', 'subforum'):
            subforum_id = tr_subforum.a['href'].split("forumid=")[-1]
            name = tr_subforum.a.text

            forum_obj = SAForum(self, subforum_id, name)

            yield forum_obj.id, forum_obj

    def _thread_obj_persist(self, thread_id, tr_thread):
        if thread_id in self.threads:
            val = self.threads[thread_id]
            val._content = tr_thread
            val._parse_tr_thread()

        else:
            val = SAThread(self, thread_id, tr_thread)

        return val