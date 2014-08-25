from sa_tools.base.sa_collection import SACollection
from sa_tools.base.descriptors import TriggerProperty
from sa_tools.parsers.forum import ForumParser
from sa_tools.thread import Thread

from collections import OrderedDict

from bs4 import BeautifulSoup


class Forum(SACollection):
    threads = TriggerProperty('read', 'threads')
    subforums = TriggerProperty('read', 'subforums')

    parser = ForumParser()

    def __init__(self, parent, id: int, *args, page: int=1, subforums: dict=None, **properties):
        super().__init__(parent, id, *args, page=page, **properties)
        self._base_url = \
            'http://forums.somethingawful.com/forumdisplay.php'
        self.url = self._base_url + '?forumid=' + str(id)
        self.threads = OrderedDict()
        self.subforums = subforums if subforums else OrderedDict()

    @property
    def is_index(self):
        index_ids = None, -1

        return self.id in index_ids

    def read(self, pg: int=1):
        super().read(pg)

        self.threads = OrderedDict()

        if self.children:
            self._subforums_from_children()

        self._apply_parser_gens(*self.parser.parse(self._content, self.id))

    def _apply_parser_gens(self, info_gen: iter, subforum_gen: iter, thread_gen: iter):
        self._apply_key_vals(info_gen)

        if subforum_gen:
            self._add_subforums(subforum_gen)

        self._add_threads(thread_gen)

    def _add_thread(self, thread_id: int, thread_content: BeautifulSoup):
        thread_obj = Thread(self, thread_id, thread_content)
        self.threads[thread_obj.id] = thread_obj

    def _add_subforum(self, forum_id: int, forum_name: str):
        forum_obj = Forum(self, forum_id, forum_name)
        self.subforums[forum_obj.id] = forum_obj

    def _add_threads(self, threads_gen: iter):
        for thread_id, content in threads_gen:
            self._add_thread(thread_id, content)

    def _add_subforums(self, subforums_gen: iter):
        for subforum_id, name in subforums_gen:
            self._add_subforum(subforum_id, name)

    def _subforums_from_children(self):
        if self.children and not self.subforums:
            for subforum in self.children:
                self.subforums[subforum.id] = subforum


def find_threads_by_name(forum: Forum, name: str) -> iter((Thread,)):
    if not forum.page:
        forum.read()

    while forum.page <= forum.pages:
        threads = forum.threads.values()

        for thread in threads:
            if name in thread.name:
                yield thread

        if forum.page == forum.pages:
            break

        else:
            forum.read(forum.pages + 1)