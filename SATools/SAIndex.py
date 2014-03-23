from SATools.SAForum import SAForum
#from SATools.SASection import SASection
#from SATools.SAObj import SAListObj
#from bs4 import BeautifulSoup
from collections import OrderedDict as ordered

class SAIndex(object):
    def __init__(self, sa_session):
        super(SAIndex, self).__init__()

        self.session = sa_session.session
        self.base_url = 'http://forums.somethingawful.com/'

        self.forums = ordered()
        self.listings = ordered()
        self.sections = None
        self._content = None
        self.json = None

        self._get_json()
        self._get_sections()

    def _save(self, section_id, sa_section):
        self.forums[section_id] = sa_section
        self.listings[section_id] = sa_section.name

    def _get_json(self):
        url = self.base_url + 'f/json/forumtree'
        request = self.session.get(url)
        self._content = request.content
        self.json = request.json()

    def _get_sections(self):
        self.sections = next(self.__gen_from_json())

    def __gen_from_json(self, json=None, parent=None):
        if json is None:
            json = self.json

        if parent is None:
            parent = self

        children = json['children']
        id = json['forumid']
        title = json['title'] if 'title' in json else 'Index'

        parent = SAForum(parent, id, name=title)
        sa_children = []

        for child in children:
            for sa_child in self.__gen_from_json(child, parent):
                sa_children.append(sa_child)

        parent.children = sa_children
        self._save(parent.id, parent)

        yield parent


