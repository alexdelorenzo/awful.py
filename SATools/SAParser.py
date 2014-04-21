from SATools.SAObj import SAObj, SAMagic
from SATools.SATypes import TriggerProperty, IntOrNone

from collections import OrderedDict as ordered
from bs4 import BeautifulSoup, element
from math import ceil, floor
from re import compile


class BSWrapper(object):
    def __init__(self, parent, *args, **kwargs):
        super(BSWrapper, self).__init__()
        self.parent = parent
        self._bs_wrappers = BeautifulSoup, element.Tag

    def wrap_parent_content(self):
        if self.content is None:
            return

        if not self._is_wrapped():
            self.content = BeautifulSoup(self.content)

    def _is_wrapped(self, content=None):
        if not content:
            content = self.content

        content_type = type(content)

        if content_type in self._bs_wrappers:
            return True
        else:
            return False

    @property
    def content(self):
        return self.parent._content

    @content.setter
    def content(self, new_val):
        self.parent._content = new_val
        self.wrap_parent_content()


class RegexManagement(SAMagic):
    def __init__(self, *args, **kwargs):
        super(RegexManagement, self).__init__(*args, **kwargs)
        self._regex_map = dict()
        self._regex_strs = dict()

    def set_regex_map(self, regex_map=None):
        if not regex_map:
            regex_map = dict()

        self._regex_map = regex_map

    def set_regex_strs(self, regex_str=None):
        if not regex_str:
            regex_str = dict()

        self._regex_str = regex_str

    def regex_lookup(self, key):
        exists = key in self.regex_map

        if exists:
            regex_c = self.regex_map[key]

        else:
            regex_str = self.regex_strs[key]
            regex_c = compile(regex_str)
            self.regex_map[key] = regex_c

        return regex_c

    def regex_matches(self, key, string):
        regex_c = self.regex_lookup(key)
        matches = regex_c.search(string).groups()

        return matches


class SAParser(SAObj):
    def __init__(self, parent, wrapper=BSWrapper, parser_map=None, *args, **kwargs):
        super(SAParser, self).__init__(parent, *args, **kwargs)
        self.id = self.parent.id
        self.wrapper = None
        self._parser_map = None

        self.set_wrapper(wrapper)
        self.set_parser_map(parser_map)
        self._delete_extra()

    def set_wrapper(self, wrapper=BSWrapper):
        self.wrapper = BSWrapper(self.parent)

        if self.parent._content:
            self.wrapper.wrap_parent_content()

    def set_parser_map(self, parser_map=None):
        if parser_map is None:
            parser_map = dict()

        self._parser_map = parser_map

    def dispatch(self, key, val=None, content=None):
        if key not in self._parser_map:
            return

        self._parser_map[key](key, val, content)

    def parse(self):
        self.read()
        self.wrapper.wrap_parent_content()

    @property
    def content(self):
        return self.wrapper.content

    @content.setter
    def content(self, new_val):
        self.wrapper.content = new_val


class SANaviParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SANaviParser, self).__init__(*args, **kwargs)

    def parse(self):
        super(SANaviParser, self).parse()

    @staticmethod
    def parse_navi(parent):
        wrapper = BSWrapper(parent)
        navi_content = wrapper.content.find('div', 'pages')

        return navi_content


class SAPageNaviParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SAPageNaviParser, self).__init__(*args, **kwargs)

    def parse(self):
        super(SAPageNaviParser, self).parse()
        self._parse_page_selector()

    def _parse_page_selector(self):
        page_selector = self.content.find_all('option')

        if len(page_selector):
            self.parent.pages = page_selector[-1].text
        else:
            self.parent.pages = 1


class SAForumParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SAForumParser, self).__init__(*args, **kwargs)

    def parse(self):
        super(SAForumParser, self).parse()

        if self.parent.is_index:
            return

        self.parse_subforums()
        self.parse_threads()

    def parse_subforums(self):
        if not self.has_subforums():
            return

        elif self.parent.children:
            self.parent._subforums_from_children()

        else:
            content = self.content
            tr_subforums = content.find_all('tr', 'subforum')

            for tr_subforum in tr_subforums:
                href = tr_subforum.a['href']
                subforum_id = href.split("forumid=")[-1]
                name = tr_subforum.a.text

                self.parent._add_subforum(subforum_id, name)

    def parse_threads(self):
        if self.unread:
            self.parse()

        self.content = self.content.find('div', id='content')
        thread_blocks = self.content.find_all('tr', 'thread', id=True)

        for tr_thread in thread_blocks:
            thread_id = IntOrNone.int_check(tr_thread['id'][6:])
            self.parent._add_thread(thread_id, tr_thread)

    def has_subforums(self):
        if self.children:
            return True

        content = self.content

        if content.table:
            return content.table['id'] == 'subforums'
        else:
            return False

class SAThreadParser(SAParser, RegexManagement):
    def __init__(self, parent, *args, **kwargs):
        super(SAThreadParser, self).__init__(parent, *args, **kwargs)
        self.set_parser_map()
        self.set_regex_map()
        self._dynamic_attr()

    def parse(self):
        super(SAThreadParser, self).parse()
        self.parse_info()
        self.parse_posts()
        self._delete_extra()

    def parse_info(self):
        self._parse_tr_thread()

    def parse_posts(self):
        posts_content = self.content.find_all('table', 'post')

        for post in posts_content:
            post_id = post['id'][4:]
            self.parent._add_post(post_id, post)

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

    def set_regex_map(self):
        super(SAThreadParser, self).set_regex_map()
        regex_strs = \
            {'lastpost': "([0-9]+:[0-9]+) ([A-Za-z 0-9]*, 20[0-9]{2})(.*)",
             'rating': "([0-9]*) votes - ([0-5][\.[0-9]*]?) average"}
        self.set_regex_strs(regex_strs)

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
            replies_url = self.base_url + link['href']
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


class SAProfileParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SAProfileParser, self).__init__(*args, **kwargs)

    def _get_profile_from_url(self):
        self.parent._fetch()
        table = self.content.find('table', 'standard')
        rows = table.find_all('tr')
        pertinent_info = rows[1]

        self.content = pertinent_info
        self.parent.read()

    def parse(self):
        if self.content:
            super(SAProfileParser, self).parse()
            self._parse_tr()

        else:
            self._get_profile_from_url()
            self._parse_contact_info()

    def _parse_tr(self):
        if not self.parent.id:
            self.parent.id = self.content.td['class'][-1]

        if self.content.img:
            self.parent.avatar_url = self.content.img['src']

        if not self.parent.name:
            self.parent.name = self.content.find('dt', 'author').text.strip()

        self.parent.title = self.content.find('dd', 'title')
        self.parent.reg_date = self.content.find('dd', 'registered').text.strip()


    def _parse_contact_info(self):
        bs_contact = self.content.find('dl', 'contacts')
        dts, dds = bs_contact.find_all('dt'), bs_contact.find_all('dd')

        contact_info = dict()
        bad_vals = 'pm', 'not set'

        for dt, dd in zip(dts, dds):
            service = dt['class'][-1]
            handle = dd.text.strip()

            good_service = service not in bad_vals
            good_handle = handle not in bad_vals
            good_pair = good_service and good_handle

            if good_pair:
                contact_info[service] = handle

        self.parent.contact_info = contact_info


class SAPostParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SAPostParser, self).__init__(*args, **kwargs)

    def parse(self):
        self._parse_from_thread()

    def _parse_from_thread(self):
        user_id = self.content.ul.a['href'].split('userid=')[-1]
        user_name = self.content.dt.text
        content = self.content.find('td', 'userinfo')
        self.parent._add_poster(user_id, user_name, content)

        has_post = self.content.find('td', 'postbody')
        self.parent.body = has_post.text.strip() if has_post else ""
