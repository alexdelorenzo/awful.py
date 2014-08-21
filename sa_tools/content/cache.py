from sa_tools.base.base import Base
from functools import lru_cache


class Cache(Base):
    forums = \
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
        super(Cache, self).__init__(*args, **kwargs)

    @lru_cache(maxsize=512)
    def get(self, *args, **kwargs):
        return self.session.get(*args, **kwargs)

    @lru_cache(maxsize=512)
    def forum_icon(self, forum_id):
        url = 'http://fi.somethingawful.com/forumicons/'
        ext = '.gif'
        forum = self.forum_dict[forum_id]

        return url + forum + ext




