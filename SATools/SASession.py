from SATools.SAObjs.SAMagic import SAMagic
from SATools.SAPoster import SAPoster
from SATools.SAReply import SAReply

from requests import Session
from bs4 import BeautifulSoup

import time


class SASession(SAMagic):
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
        self.replies = []

        self.logged_in_at = time.strftime('%x @ %X', time.localtime())
        self.name = 'Session: login(), reply(), post_thread(), search(), etc'

    def __getstate__(self):
        if self.profile:
            del self.profile

        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._set_profile()

    def _set_user_agent(self):
        ua = "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1"
        self.session.headers['User-Agent'] = ua

    def _set_profile(self):
        self.profile = SAPoster(self, self.id, name=self.username)

    def login(self, username, passwd):
        login_url = self._base_url + 'account.php'
        post_data = {'username': username, 'password': passwd, 'action': 'login'}

        response = self.session.post(login_url, post_data)

        if not response.ok:
            raise Exception(("Unable to login", response.status_code, response.reason))

        self.logged_in_at = time.strftime('%x @ %X', time.localtime())

    def reply(self, _id, body):
        sa_reply = SAReply(self, id=_id, body=body)
        sa_reply.reply()
        self.replies.append(sa_reply)

    def post_thread(self, forumid, title, body, tag=None, poll=None):
        raise NotImplementedError()

    def find_user_posts(self, user_id):
        raise NotImplementedError()

    def search(self):
        raise NotImplementedError()