from sa_tools.base.magic import MagicMixin
from sa_tools.poster import Poster
from sa_tools.reply import Reply

from requests import Session
from bs4 import BeautifulSoup

import time


class SASession(MagicMixin):
    def __init__(self, username, passwd):
        super(SASession, self).__init__(None)
        self.session = Session()
        self._set_user_agent()
        self.username = username
        self._base_url = 'https://forums.somethingawful.com/'
        self.login(username, passwd)
        self.id = self.session.cookies.get('bbuserid')
        self.profile = None
        self._set_profile()

        self.name = 'Session: login(), reply(), post_thread(), search(), etc'

    def _set_user_agent(self):
        identity = "Mozilla/5.0"
        system = "(Windows NT 6.2; Win64; x64; rv:16.0.1)"
        engine = "Gecko/20121011"
        version = "Firefox/16.0.1"
        strs = identity, system, engine, version
        ua = ' '.join(strs)

        self.session.headers['User-Agent'] = ua

    def _set_profile(self):
        self.profile = Poster(self, self.id, name=self.username)

    def login(self, username, passwd):
        login_url = self._base_url + 'account.php'

        post_data = {'action': 'loginform'}
        form_data = {'username': username,
                     'password': passwd,
                     'action': 'login',
                     'next': '/'}

        response = self.session.post(login_url, params=post_data, data=form_data)

        if not response.ok:
            raise Exception(("Unable to login", response.status_code, response.reason))

        self.logged_in_at = time.strftime('%x @ %X', time.localtime())

    def reply(self, _id, body):
        sa_reply = Reply(self, id=_id, body=body)
        sa_reply.reply()

    def post_thread(self, forum_id, title, body, tag=None, poll=None):
        raise NotImplementedError()

    def find_user_posts(self, user_id):
        raise NotImplementedError()

    def search(self):
        raise NotImplementedError()