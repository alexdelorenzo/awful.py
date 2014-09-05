from sa_tools.base.magic import MagicMixin
from sa_tools.poster import Poster
from sa_tools.reply import Reply

from requests import Session, Response
from bs4 import BeautifulSoup
import dataset

import time


def cache(func):
    def new(url, params=None, **kwargs):
        db = dataset.connect('sqlite:///test.db')
        response = func(url, params, **kwargs)
        row = {'url': url, 'params': params, 'response': response}
        db['requests'].insert(row)

        return response
    return new


class SASession(Session, MagicMixin):
    _base_url = 'https://forums.somethingawful.com/'
    name = 'awful_py Session'

    def __init__(self, username: str, passwd: str):
        super().__init__()

        self.session = self
        self.session.headers['User-Agent'] = user_agent()

        self.username = username
        self.login(username, passwd)
        self.login_time = time.strftime('%x @ %X', time.localtime())

        self.id = self.session.cookies.get('bbuserid')
        self.profile = None
        self._set_profile()

    def get(self, url: str, *args, **kwargs) -> Response:
        return super().get(url, **kwargs)

    def post(self, url: str, *args, **kwargs) -> Response:
        return super().post(url, *args, **kwargs)

    def _set_profile(self):
        self.profile = Poster(self, self.id, name=self.username)

    def login(self, username: str, passwd: str) -> Response:
        return login(self.session, username, passwd, self._base_url)

    def reply(self, id: int, body: str) -> Reply:
        return reply(self, id, body)

    def pm(self, username: str, title: str="(no title)", body: str="", tag: int=420) -> Response:
        return pm(self.session, username, title, body, tag)

    def post_thread(self, forum_id: int, title: str, body: str, tag: int=None, poll: dict=None):
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


def reply(parent, id: int, body: str) -> Reply:
    sa_reply = Reply(parent, id=id, body=body)
    sa_reply.reply()

    return sa_reply


def pm(session: Session, recv_username: str, title: str="", body: str=None, tag: int=420) -> Response:
    url = "http://forums.somethingawful.com/private.php"
    #params = {'action': 'newmessage'}
    #response = session.get(url, params=params)

    data = {'action': 'dosend',
            'prevmessageid': "",
            'forward': "",
            'touser': recv_username,
            'title': title,
            'iconid': tag,
            'message': body,
            'parseurl': 'yes',
            'savecopy': 'yes',
            'submit': 'Send+Message'}

    response = session.post(url, data=data)

    return response