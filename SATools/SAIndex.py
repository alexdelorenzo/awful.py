from SATools.SAForum import SAForum
from SATools.SAObj.SAMagic import SAMagic
from SATools.SASection import SASection

from collections import OrderedDict as ordered

class SAIndex(SAMagic):
    def __init__(self, sa_session):
        super(SAIndex, self).__init__(sa_session)
        self.name = "Forums' index"

        self.session = sa_session.session
        self._base_url = 'http://forums.somethingawful.com/'
        self.url = self._base_url
        self.forums = ordered()
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

        self.sections = SASection(parent, id=_id, name=name, children=children)
        self._save(self.sections.id, self.sections)

    def __gen_from_json(self, json=None, parent=None):
        if json is None:
            json = self._json

        if parent is None:
            parent = self

        children = json['children']
        forum_id = json['forumid'] if json['forumid'] else None
        title = json['title'] if 'title' in json else 'Index'

        parent = SAForum(parent, id=forum_id, name=title)
        sa_children = []

        for child in children:
            for sa_child in self.__gen_from_json(child, parent):
                sa_children.append(sa_child)

        parent.children = sa_children
        self._save(parent.id, parent)

        yield parent