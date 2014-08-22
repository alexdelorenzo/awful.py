from sa_tools.base.magic import MagicMixin
from sa_tools.poster import Poster
from sa_tools.reply import Reply

from requests import Session, Response
from bs4 import BeautifulSoup

import time


class SASession(MagicMixin):
    def __init__(self, username: str, passwd: str):
        super().__init__()
        self.session = Session()
        self.session.headers['User-Agent'] = user_agent()
        self.username = username
        self._base_url = 'https://forums.somethingawful.com/'

        self.login(username, passwd)
        self.logged_in_at = time.strftime('%x @ %X', time.localtime())

        self.id = self.session.cookies.get('bbuserid')
        self.profile = None
        self._set_profile()
        self.name = 'Session: login(), reply(), post_thread(), search(), etc'

    def _set_profile(self):
        self.profile = Poster(self, self.id, name=self.username)

    def login(self, username: str, passwd: str) -> Response:
        return login(self.session, username, passwd, self._base_url)

    def reply(self, _id: int, body: str) -> Reply:
        sa_reply = Reply(self, id=_id, body=body)
        sa_reply.reply()

        return sa_reply

    def post_thread(self, forum_id: int, title: str, body: str, tag: str=None, poll: dict=None):
        raise NotImplementedError()

    def find_user_posts(self, user_id):
        raise NotImplementedError()

    def search(self):
        raise NotImplementedError()


def login(session: Session, username: str, passwd: str, url: str) -> Response:
    login_url = url + 'account.php'

    post_data = {'action': 'loginform'}
    form_data = {'username': username,
                 'password': passwd,
                 'action': 'login',
                 'next': '/'}

    response = session.post(login_url, params=post_data, data=form_data)

    if not response.ok:
        raise Exception(("Unable to login", response.status_code, response.reason))

    return response


def user_agent() -> str:
    identity = "Mozilla/5.0"
    system = "(Windows NT 6.2; Win64; x64; rv:16.0.1)"
    engine = "Gecko/20121011"
    version = "Firefox/16.0.1"
    strs = identity, system, engine, version

    return ' '.join(strs)