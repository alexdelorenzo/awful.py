from SATools.SAThread import SAThread
from SATools.SAObj import SAListObj
from SATools.SATypes import TriggerProperty, IntOrNone
from SATools.SAParser import SAForumParser

from collections import OrderedDict as ordered


class SAForum(SAListObj):
    threads = TriggerProperty('read', 'threads')
    subforums = TriggerProperty('read', 'subforums')

    def __init__(self, parent, id, content=None, name=None,
                 page=1, subforums=None, **properties):
        super(SAForum, self).__init__(parent, id, content, name, page=page, **properties)
        self.base_url = \
            'http://forums.somethingawful.com/forumdisplay.php'
        self.url = self.base_url + '?forumid=' + str(id)
        self.parser = SAForumParser(self)

        self.threads = ordered()
        self.subforums = subforums if subforums else ordered()

    def read(self, pg=1):
        if self.is_index:
            self.unread = False
            return

        super(SAForum, self).read(pg)
        self._threads_persist(parse=True)

    @property
    def is_index(self):
        index_ids = None, -1
        return self.id in index_ids

    def _add_thread(self, thread_id, thread_content):
        sa_thread = self._thread_obj_persist(thread_id, thread_content)
        self.threads[sa_thread.id] = sa_thread

    def _add_subforum(self, forum_id, forum_name):
        forum_obj = SAForum(self, forum_id, forum_name)
        self.subforums[forum_obj.id] = forum_obj

    def _threads_persist(self, parse=True):
        """
        This monkey patch can be eliminated.
        """

        self._old_threads = self.threads
        self.threads = ordered()

        if parse:
            self.parser.parse()

        self._old_threads = None
        self._delete_extra()

    def _thread_obj_persist(self, thread_id, tr_thread):
        threads_exist = self._old_threads

        if threads_exist:
            is_in_old = thread_id in threads_exist
        else:
            is_in_old = False

        if is_in_old:
            val = self._old_threads[thread_id]
            val.parser.wrapper.content = tr_thread
            val.parser.parse_info()

        else:
            val = SAThread(self, thread_id, tr_thread)

        return val

    def _subforums_from_children(self):
        if self.children and not self.subforums:
            for subforum in self.children:
                _id = subforum.id
                self.subforums[_id] = subforum
