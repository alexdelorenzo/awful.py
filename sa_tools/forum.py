from sa_tools.base.sa_collection import SACollection
from sa_tools.base.descriptors import TriggerProperty
from sa_tools.parsers.forum import ForumParser
from sa_tools.thread import Thread

from collections import OrderedDict as ordered


class Forum(SACollection):
    threads = TriggerProperty('read', 'threads')
    subforums = TriggerProperty('read', 'subforums')

    def __init__(self, parent, id, content=None, name=None,
                 page=1, subforums=None, **properties):
        super(Forum, self).__init__(parent, id, content, name, page=page, **properties)
        self._base_url = \
            'http://forums.somethingawful.com/forumdisplay.php'
        self.url = self._base_url + '?forumid=' + str(id)
        self.parser = ForumParser(self)
        self.threads = ordered()
        self.subforums = subforums if subforums else ordered()

    def read(self, pg=1):
        if self.is_index:
            self.unread = False
            return

        super(Forum, self).read(pg)

        info_gen, subforum_gen, thread_gen = self.parser.parse(self._content)

        if subforum_gen:
            self._add_subforums(subforum_gen)

        self._add_threads(thread_gen)
        self._apply_key_vals(info_gen)

    @property
    def is_index(self):
        index_ids = None, -1
        return self.id in index_ids

    def _add_thread(self, thread_id, thread_content):
        #sa_thread = self._thread_obj_persist(thread_id, thread_content)
        sa_thread = Thread(self, thread_id, thread_content)
        self.threads[sa_thread.id] = sa_thread

    def _add_threads(self, threads_gen):
        for thread_id, content in threads_gen:
            self._add_thread(thread_id, content)

    def _add_subforums(self, subforums_gen):
        for subforum_id, name in subforums_gen:
            self._add_subforum(subforum_id, name)

    def _add_subforum(self, forum_id, forum_name):
        forum_obj = Forum(self, forum_id, forum_name)
        self.subforums[forum_obj.id] = forum_obj

    def _subforums_from_children(self):
        if self.children and not self.subforums:
            for subforum in self.children:
                _id = subforum.id
                self.subforums[_id] = subforum

    # def _threads_persist(self, parse=True):
    #     # TODO: get rid of this shit
    #
    #     self._old_threads = self.threads
    #     self.threads = ordered()
    #
    #     if parse:
    #         self.parser.parse(self._content)
    #
    #     self._old_threads = None
    #     self._delete_extra()
    #
    # def _thread_obj_persist(self, thread_id, tr_thread):
    #     #TODO: seriously get rid of it
    #     threads_exist = self._old_threads
    #
    #     if threads_exist:
    #         is_in_old = thread_id in threads_exist
    #
    #     else:
    #         is_in_old = False
    #
    #     if is_in_old:
    #         val = self._old_threads[thread_id]
    #         val.parser.wrapper.content = tr_thread
    #         val.parser.parse_info()
    #
    #     else:
    #         val = Thread(self, thread_id, tr_thread)
    #
    #     return val