from sa_tools.parsers.parser import Parser
from sa_tools.base.descriptors import IntOrNone
from sa_tools.session import SASession, Session

from requests import Session
from bs4 import Tag, BeautifulSoup
from functools import singledispatch


class ForumParser(Parser):
    forum_ids = \
        dict([(1, 'gbs'),
             (26, 'fyad'),
             (268, 'byob'),
             (44, 'games'),
             (192, 'iyg'),
             (158, 'at'),
             (46, 'dnd'),
             (22, 'shsc'),
             (122, 'sas'),
             (179, 'ylls'),
             (242, 'pac'),
             (161, 'gws'),
             (167, 'pyf'),
             (91, 'ai'),
             (124, 'pi'),
             (132, 'tfr'),
             (90, 'tcc'),
             (218, 'terrordome'),
             (31, 'cc'),
             (151, 'cd'),
             (182, 'tbb'),
             (150, 'nmd'),
             (130, 'tviv'),
             (144, 'bss'),
             (27, 'adtrw'),
             (215, 'phiz'),
             (255, 'RGD'),
             (61, 'samart'),
             (43, 'gag'),
             (241, 'citysucks'),
             (188, 'qcs'),
             (21, 'goldmine'),
             (25, 'gas')])

    def __init__(self, *args, **kwargs):
        super(ForumParser, self).__init__(*args, **kwargs)

    def parse(self, content: Tag) -> (iter, iter, iter):
        super(ForumParser, self).parse()

        if self.parent.is_index:
            return

        if self.parent.children:
            self.parent._subforums_from_children()

        info_gen = parse_info(self.id, self.forum_ids)
        subforums_gen = \
            parse_subforums(content) if has_subforums(content) else None
        threads_gen = parse_threads(content)

        return info_gen, subforums_gen, threads_gen


def parse_subforums(content: Tag) -> (str, str):
    tr_subforums = content.find_all('tr', 'subforum')

    for tr_subforum in tr_subforums:
        href = tr_subforum.a['href']
        subforum_id = href.split("forumid=")[-1]
        name = tr_subforum.a.text

        yield subforum_id, name


def parse_threads(content: Tag) -> (int, Tag):
    content = content.find('div', id='content')
    thread_blocks = content.find_all('tr', 'thread', id=True)

    for tr_thread in thread_blocks:
        thread_id = IntOrNone.int_check(tr_thread['id'][6:])

        yield thread_id, tr_thread


def parse_info(forum_id, forum_dict) -> (str, str):
    yield 'icon_url', forum_icon(forum_id, forum_dict)


def get_icon_map(session: Session) -> (int, str):
    index = session.get("http://forums.somethingawful.com")
    bs_index = BeautifulSoup(index.content)
    forums = bs_index.find_all('tr', 'forum')

    for forum in forums:
        forum_id = int(forum.a['href'].split('=')[-1])
        forum_acronym = forum.img['src'].split('/')[-1].split('.')[0]

        yield forum_id, forum_acronym


def has_subforums(content: Tag) -> bool:
    if content.table:
        return content.table['id'] == 'subforums'

    else:
        return False


def forum_icon(forum_id: int, forum_dict: dict, session: Session=None) -> str or None:
    url = 'http://fi.somethingawful.com/forumicons/'
    ext = '.gif'

    if forum_id in forum_dict:
        forum = forum_dict[forum_id]

    else:
        if session is None:
            return None

        else:
            return forum_icon(forum_id, dict(get_icon_map(session)))

    return url + forum + ext
