from sa_tools.parsers.parser import Parser
from sa_tools.base.descriptors import IntOrNone

from bs4 import Tag


class ForumParser(Parser):
    def __init__(self, *args, **kwargs):
        super(ForumParser, self).__init__(*args, **kwargs)

    def parse(self):
        super(ForumParser, self).parse()

        if self.parent.is_index:
            return

        if self.parent.children:
            self.parent._subforums_from_children()

        subforums_gen = \
            parse_subforums(self.content) if has_subforums(self.content) else None
        threads_gen = parse_threads(self.content)

        return subforums_gen, threads_gen


def parse_subforums(content: Tag):
    tr_subforums = content.find_all('tr', 'subforum')

    for tr_subforum in tr_subforums:
        href = tr_subforum.a['href']
        subforum_id = href.split("forumid=")[-1]
        name = tr_subforum.a.text

        yield subforum_id, name


def parse_threads(content: Tag):
    content = content.find('div', id='content')
    thread_blocks = content.find_all('tr', 'thread', id=True)

    for tr_thread in thread_blocks:
        thread_id = IntOrNone.int_check(tr_thread['id'][6:])
        yield thread_id, tr_thread


def has_subforums(content: Tag):
    if content.table:
        return content.table['id'] == 'subforums'

    else:
        return False