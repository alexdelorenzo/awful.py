from bs4 import BeautifulSoup

from sa_tools.base.list_obj import SAListObj
from sa_tools.search import search_result
from sa_tools.parsers.search import SASearchParser


class SASearch(SAListObj):
    def __init__(self, parent, query, q_type=None, **options):
        super(SASearch, self).__init__(parent, id=None, name=query, **options)
        self._base_url = "http://forums.somethingawful.com/search.php"
        self.query = query
        self.type = type
        self.results = None
        self.parser = SASearchParser(self)

    def read(self, pg=1):
        super(SASearch, self).read(pg)

        self.parser.parse()

        for result in self.results:
            result.read()
            result.get_post()

    def search_profile(self, sa_profile):
        self.search_userid(sa_profile.id)

    def search_userid(self, user_id):
        params = {'action': 'do_search_posthistory', 'userid': str(user_id)}
        param_str = '&'.join([key + '=' + val for key, val in params.items()])
        url = self._base_url + '?' + param_str

        response = self.session.post(url)
        response = self._jump(response)

        self.parser.content = BeautifulSoup(response.text)
        self._parse_search_results()


    def _jump(self, response, base_url=None):
        if not base_url:
            base_url = self._base_url

        bs_content = BeautifulSoup(response.text)
        request_id = bs_content.head.meta['content'].lower()
        request_id = request_id.split('url=').pop()
        jump_url = base_url + request_id
        self.url = jump_url

        return self.session.get(jump_url)


class SASearchNewStyle(SAListObj):
    def __init__(self, query, type, session, **options):
        super(SASearchNewStyle, self).__init__(name=query, session=session, **options)
        self._base_url = "http://forums.somethingawful.com/f/search"
        self.query = query
        self.lihllllltype = type
        self.results = None

        self.options = \
            {'forumids': '',
             'groupmode': 0,
             'keywords': '',
             'opt_search_posts': 'on',
             'opt_search_titles': 'on',
             'perpage': 50,
             'search_mode': 'ext',
             'uf_posts': 'on',
             'userid_filters': 0,
             'username_filter': '',
             'show_post_previews': 0}

        for name, option in options.items():
            if name in self.options:
                self.options[name] = option

    def read(self, pg=1):
        super().read(pg)

        for result in self.results:
            result.read()

    def search_by_user(self, sa_poster, keywords=""):
        self.options['userid_filter'] = sa_poster.id
        self.options['keywords'] = keywords
        self.search()

    def search(self):
        url = self._base_url + '/submit'
        response = self.session.post(url, self.options)
        bs = BeautifulSoup(response.content)
        response = self._jump(response, url)

        return response

    def group_by(self, option='post'):
        options = {'post': 0,
                   'thread': 1,
                   'forum': 2}

        if option not in options:
            return False

        self.options['groupmode'] = options[option]

    def sort_by(self, option='relevance'):
        options = {'relevance': 0,
                   'rel': 0,
                   'date': 1,
                   'match': 2,
                   'word': 3}

        if option not in options:
            return False

        self.options['sort'] = options[option]

    def _jump(self, response, base_url=None):
        if not base_url:
            base_url = self._base_url

        bs_content = BeautifulSoup(response.text)
        request_id = bs_content.head.meta['content'].lower()
        request_id = request_id.split('qid=').pop()
        jump_url = self._base_url + request_id
        self.url = jump_url

        return self.session.get(jump_url)