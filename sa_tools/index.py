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

    def _save(self, section_id, sa_section):
        self.forums[section_id] = sa_section

    def _get_json(self):
        url = self._base_url + 'f/json/forumtree'
        request = self.session.get(url)

        self._content = request.content
        self._json = request.json()

    def _get_sections(self):
        section = next(self.__gen_from_json())
        parent, _id, name, children = \
            section.parent, section.id, section.name, section.children

        self.sections = SASection(parent, _id, name=name, children=children)
        self.forums.pop(self.sections.id)

    def __gen_from_json(self):
        return gen_from_json(self._json, self, self.forums)


def gen_from_json(json: dict=None, parent: Forum=None, flat_dict: dict=None) -> iter((Forum,)):
    children = json['children']
    forum_id = json['forumid'] if json['forumid'] else None
    title = json['title'] if 'title' in json else 'Index'

    parent = Forum(parent, id=forum_id, name=title)

    sa_children = []
    for child in children:
        for sa_child in gen_from_json(child, parent, flat_dict):
            sa_children.append(sa_child)

    parent.children = sa_children

    if flat_dict is not None:
        flat_dict[parent.id] = parent

    yield parent