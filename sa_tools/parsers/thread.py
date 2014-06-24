from sa_tools.parsers.tools.regex_manager import RegexManager
from sa_tools.parsers.parser import Parser

from collections import OrderedDict as ordered
from math import ceil


class ThreadParser(Parser, RegexManager):
    def __init__(self, parent, *args, **kwargs):
        super(ThreadParser, self).__init__(parent, *args, **kwargs)
        self._dynamic_attr()
        self.post_gen = None

    def parse(self):
        super(ThreadParser, self).parse()
        self.parse_info()
        self.post_gen = self.parse_posts(self.content)

        self._delete_extra()

        return self.results

    def parse_info(self):
        if self.content:
            self._parse_tr_thread()

        else:
            self._parse_from_url()

    def parse_posts(self, content=None):
        posts_content = content.find_all('table', 'post')
        post_gen = ((post['id'][4:], post) for post in posts_content)

        return post_gen

    def set_parser_map(self, parser_map=None):
        if not parser_map:
            parser_map = \
                {'icon': self._parse_icon,
                 'lastpost': self._parse_last_post,
                 'replies': self._parse_replies,
                 'author': self._parse_author,
                 'title': self._parse_title,
                 'title_sticky': self._parse_title,
                 'views': self._parse_views,
                 'rating': self._parse_rating}

        super(ThreadParser, self).set_parser_map(parser_map)

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

        super(ThreadParser, self).set_regex_strs(regex_strs)

    def _parse_from_url(self):
        self.parent.read()
        self._parse_first_post()
        title = self.content.find('a', 'bclast').text.strip()
        self.parent.title = title

    def _parse_first_post(self, post_content=None):
        if not post_content:
            post_content = self.content.find('table', 'post')

        post_id = post_content['id'][4:]
        result = post_id, post_content, True

        self.results['op'] = result

    def _parse_tr_thread(self, content=None):
        if not self.content:
            return

        tds = self.content.find_all('td')
        gen_name_content = ((td['class'][-1], td.text.strip(), td)
                            for td in tds)
        gen_key_val = (self.dispatch(*attr_val)
                       for attr_val in gen_name_content)
        #self.results += dict(gen_key_val)

        for td in tds:
            td_class = td['class'][-1]
            text = td.text.strip()

            self.dispatch(td_class, text, td)

    def _parse_icon(self, key, val, content):
        text = content.a['href'].split('posticon=')[-1]

        self.results[key] = text

    def _parse_last_post(self, key, val, content):
        groups = 'time', 'date', 'user'
        matches = self.regex_matches(key, val)
        matches = dict(zip(groups, matches))

        self.results[key] = matches
        return key, matches

    def _parse_author(self, key, val, content):
        link = content.a
        author = link.text.strip()
        user_id = link['href'].split('id=')[-1]
        result = user_id, author
        self.results[key] = result
        return key, result

    def _parse_replies(self, key, val, content):
        self._parse_page_count(val)

        reply_count = int(content.text.strip())

        self.results[key] = reply_count
        return key, reply_count

        # link = content.a
        #
        # if link:
        #     replies_url = self._base_url + link['href']
        #     replies_count = int(content.a.text.strip())
        #     replies = {'url': replies_url,
        #                'count': replies_count}
        #     setattr(self, key, replies)

    def _parse_views(self, key, val, content):
        views = int(content.text.strip())

        self.results[key] = views
        return key, views

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

            self.results[key] = rating

        else:
            rating = {}

        return key, rating

    def _parse_title(self, key, val, content):
        text = content.find('a', 'thread_title').text
        key = 'title'

        self.results[key] = text
        self.results['name'] = text
        return key, text

    def _parse_last_seen(self, content):
        last_read = content.find('div', 'lastseen')
        key = 'last_read'

        self.results[key] = last_read
        return key, last_read

    def _parse_page_count(self, val):
        pages = ceil(int(val) / 40.0)
        key = 'pages'

        self.results[key] = pages