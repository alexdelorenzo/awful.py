from SATools.SAParsers.RegexManager import RegexManager
from SATools.SAParsers.SAParser import SAParser

from collections import OrderedDict as ordered
from math import ceil


class SAThreadParser(SAParser, RegexManager):
    def __init__(self, parent, *args, **kwargs):
        super(SAThreadParser, self).__init__(parent, *args, **kwargs)
        self._dynamic_attr()

    def parse(self):
        super(SAThreadParser, self).parse()
        self.parse_info()
        self.parse_posts()
        self._delete_extra()

    def parse_info(self):
        if self.content:
            self._parse_tr_thread()

        else:
            self._parse_from_url()

    def parse_posts(self):
        posts_content = self.content.find_all('table', 'post')

        for post in posts_content:
            post_id = post['id'][4:]
            self.parent._add_post(post_id, post)

    def _parse_from_url(self):
        self.parent.read()
        self._parse_first_post()
        title = self.content.find('a', 'bclast').text.strip()
        self.parent.title = title

    def _parse_first_post(self, post_content=None):
        if not post_content:
            post_content = self.content.find('table', 'post')

        post_id = post_content['id'][4:]

        #TODO: pull this out into SAThread._add_first_post()
        self.parent._add_post(post_id, post_content)
        sa_post = self.parent.posts.popitem(0)[-1]
        self.parent.poster = sa_post.poster


    def set_parser_map(self, parser_map=None):
        if not parser_map:
            parser_map = \
                {'icon': self._parse_icon,
                 'lastpost': self._parse_lastpost,
                 'replies': self._parse_replies,
                 'author': self._parse_author,
                 'title': self._parse_title,
                 'title_sticky': self._parse_title,
                 'views': self._parse_views,
                 'rating': self._parse_rating}

        super(SAThreadParser, self).set_parser_map(parser_map)

    def set_regex_map(self, regex_map=None):
        if regex_map is None:
            regex_map = dict()

        super(SAThreadParser, self).set_regex_map(regex_map)

    def set_regex_strs(self, regex_strs=None):
        dicts = dict, ordered
        is_dict = isinstance(regex_strs, dicts)

        if not is_dict:
            lastpost, rating = \
                "([0-9]+:[0-9]+) ([A-Za-z 0-9]*, 20[0-9]{2})(.*)", \
                "([0-9]*) votes - ([0-5][\.[0-9]*]?) average"

            regex_strs = \
                {'lastpost': lastpost,
                 'rating': rating}

        super(SAThreadParser, self).set_regex_strs(regex_strs)

    def _parse_tr_thread(self):
        if not self.content:
            return

        for td in self.content.find_all('td'):
            td_class = td['class'][-1]
            text = td.text.strip()

            self.dispatch(td_class, text, td)

    def _parse_icon(self, key, val, content):
        text = content.a['href'].split('posticon=').pop(-1)
        setattr(self.parent, key, text)

    def _parse_lastpost(self, key, val, content):
        groups = 'time', 'date', 'user'
        matches = self.regex_matches(key, val)
        matches = dict(zip(groups, matches))
        setattr(self.parent, key, matches)

    def _parse_author(self, key, val, content):
        link = content.a
        author = link.text.strip()
        user_id = link['href'].split('id=')[-1]
        self.parent._add_author(user_id, author)

    def _parse_replies(self, key, val, content):
        self._parse_pagecount(val)
        link = content.a

        if link:
            replies_url = self._base_url + link['href']
            replies_count = int(content.a.text.strip())
            replies = {'url': replies_url,
                       'count': replies_count}
            setattr(self.parent, key, replies)

    def _parse_views(self, key, val, content):
        views = int(content.text.strip())
        setattr(self.parent, key, views)

    def _parse_rating(self, key, val, content):
        img_tag = content.img

        if img_tag:
            title_attr = img_tag['title'].strip()

            votes, avg = self.regex_matches(key, title_attr)
            votes = int(votes)
            avg = float(avg)
            stars = round(avg)

            rating = {'votes': votes,
                      'avg': avg,
                      'stars': stars}
            setattr(self.parent, key, rating)

    def _parse_title(self, key, val, content):
        text = content.find('a', 'thread_title').text
        key = 'title'

        self._parse_lastseen(content)
        setattr(self.parent, key, text)

    def _parse_lastseen(self, content):
        last_read = content.find('div', 'lastseen')
        self.parent._add_last_read(last_read)

    def _parse_pagecount(self, val):
        pages = ceil(int(val) / 40.0)
        key = 'pages'
        setattr(self.parent, key, pages)