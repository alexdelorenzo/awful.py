from sa_tools.forum import Forum
from sa_tools.base.magic import MagicMixin
from sa_tools.section import SASection

from collections import OrderedDict


class Index(MagicMixin):
    def __init__(self, sa_session, *args, **kwargs):
        super().__init__(sa_session, *args, **kwargs)

        self.name = "Forum index"
        self.session = sa_session.session
        self._base_url = 'http://forums.somethingawful.com/'
        self.url = self._base_url

        self.forums = OrderedDict()
        self.sections = None
        self._content = None
        self._json = None

        self._get_json()
        self._get_sections()

    def __repr__(self):
        forum_ct = str(len(self.forums)) + ' total forums'
        repr_str = self.name + ' containing ' + forum_ct

        return repr_str

    def _save(self, section_id: int, sa_section: SASection):
        self.forums[section_id] = sa_section

    def _get_json(self):
        url = self._base_url + 'f/json/forumtree'
        request = self.session.get(url)

        self._content = request.content
        self._json = request.json()

    def _get_sections(self):
        section = self.__forums_from_json()
        parent, _id, name, children = \
            section.parent, section.id, section.name, section.children

        self.sections = SASection(parent, _id, name=name, children=children)
        self.forums.pop(self.sections.id)

    def __forums_from_json(self):
        return forums_from_json(self._json, self, self.forums)


def forums_from_json(json: dict=None, parent: Forum=None, forum_dict: dict=None) -> iter((Forum,)):
    forum_id = json['forumid'] if json['forumid'] else None
    title = json['title'] if 'title' in json else 'Index'
    children = json['children']

    parent = Forum(parent, id=forum_id, name=title)
    parent.children = [forums_from_json(child, parent, forum_dict)
                       for child in children]

    if forum_dict is not None:
        forum_dict[parent.id] = parent

    return parent