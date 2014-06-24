from sa_tools.parsers.parser import SAParser

from bs4 import BeautifulSoup


class SASearchResultParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SASearchResultParser, self).__init__(*args, **kwargs)

    def get_post(self):
        if self.parent.unread:
            self.parent.read()

        post_id = self.parent.url.split('#')[-1][4:]
        response = self.session.get(self.url)
        bs_content = BeautifulSoup(response.text)
        post_content = bs_content.find('table', id=post_id)

        self._add_post(post_id, post_content)

    def parse(self):
        super(SASearchResultParser, self).parse()
        self.get_post()
        self._parse_content()

    def _parse_content(self):
        tds = self._content.find_all('td')
        self.parent._columns = dict(zip(self.parent.header, tds))
        self._parse_topic()
        self._parse_meta_data()

    def _parse_topic(self):
        tag_td, snippet_td = self.parent._columns['Topic'], self.parent._columns['Snippet']
        self.parent.tag_url = tag_td.img['src']
        thread_url = snippet_td.a['href']
        thread_id = thread_url.split('threadid=')[-1]
        thread_title = snippet_td.a.text
        self.parent._add_thread(thread_id, thread_title)

        preview = snippet_td.div
        self.parent.body = preview.text

        snippet_url = snippet_td.find('div', 'smalltext').a['href']
        post_url = 'http://forums.somethingawful.com/' + snippet_url
        self.parent.url = post_url

    def _parse_meta_data(self):
        forum_td = self.parent._columns['Forum']
        forum_id = forum_td.a['href'].split('forumid=')[-1]
        forum_name = forum_td.a.text
        self.parent._add_forum(forum_id, forum_name)

        author_td = self._columns['Author']
        user_id = author_td.a['href'].split('userid=')[-1]
        username = author_td.a.text
        self.parent._add_poster(user_id, username)

        self.replies = self._columns['Replies'].text
        self.views = self._columns['Views'].text
        self.date = self._columns['Date'].text