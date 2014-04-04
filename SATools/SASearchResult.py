from SATools.SAObj import SAObj
from SATools.SAThread import SAThread
from SATools.SAForum import SAForum
from SATools.SAPoster import SAPoster
from SATools.SAPost import SAPost
from bs4 import BeautifulSoup



class SASearchResult(SAObj):
    def __init__(self, parent=None, id=None, name=None, content=None, **properties):
        super(SASearchResult, self).__init__(parent, id, name=name, content=content, **properties)
        self.header = self.parent._table_header
        self.forum = None
        self.poster = None
        self.replies = None
        self.views = None
        self.date = None
        self.post = None

    def read(self):
        self._parse_content()
        self.unread = False
        del self._columns

    def get_post(self):
        if self.unread:
            self.read()

        post_id = self.url.split('#')[-1]
        print(post_id)
        response = self.session.get(self.url)
        bs_content = BeautifulSoup(response.text)
        post_content = bs_content.find('table', id=post_id)
        self.post = SAPost(self, post_id[4:], post_content)

    def _parse_content(self):
        tds = self._content.find_all('td')
        self._columns = dict(zip(self.header, tds))
        self._parse_topic()
        self._parse_meta_data()

    def _parse_topic(self):
        tag_td, snippet_td = self._columns['Topic'], self._columns['Snippet']
        self.tag_url = tag_td.img['src']
        thread_url = snippet_td.a['href']
        thread_id = thread_url.split('threadid=')[-1]
        thread_title = snippet_td.a.text

        preview = snippet_td.div
        self.body = preview.text

        snippet_url = snippet_td.find('div', 'smalltext').a['href']
        post_url = 'http://forums.somethingawful.com/' + snippet_url
        self.url = post_url

    def _parse_meta_data(self):
        forum_td = self._columns['Forum']
        forum_id = forum_td.a['href'].split('forumid=')[-1]
        forum_name = forum_td.a.text
        self.forum = SAForum(self, forum_id, name=forum_name)

        author_td = self._columns['Author']
        user_id = author_td.a['href'].split('userid=')[-1]
        username = author_td.a.text
        self.poster = SAPoster(self, user_id, name=username)

        self.replies = self._columns['Replies'].text
        self.views = self._columns['Views'].text
        self.date = self._columns['Date'].text