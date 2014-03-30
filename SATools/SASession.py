from SATools.SAPoster import SAPoster
from SATools.SASearch import SASearch

from requests import Session
from bs4 import BeautifulSoup


class SASession(object):
    def __init__(self, username, passwd):
        super(SASession, self).__init__()
        self.session = Session()
        self.username = username
        self.base_url = 'https://forums.somethingawful.com/'
        self.login(username, passwd)
        self.id = self.session.cookies.get('bbuserid')
        self.profile = None
        self._set_profile()

    def __getstate__(self):
        if self.profile:
            del self.profile

        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._set_profile()

    def _set_profile(self):
        self.profile = SAPoster(self, self.id, name=self.username)

    def login(self, username, passwd):
        login_url = self.base_url + 'account.php'
        post_data = {'username': username, 'password': passwd, 'action': 'login'}

        response = self.session.post(login_url, post_data)

        if not response.ok:
            raise Exception(("Unable to login", response.status_code, response.reason))

    def reply(self, _id, body):
        url = "http://forums.somethingawful.com/newreply.php?action=newreply&threadid=" + str(_id)

        response = self.session.get(url)
        bs = BeautifulSoup(response.content)

        inputs = {i['name']: i['value']
                  for i in bs.find_all('input')
                  if i.has_attr('value')}
        inputs['message'] = str(body)
        inputs.pop('preview')

        response = self.session.post(url, inputs)

        if not response.ok:
            raise Exception(("Unable to reply", response.status_code, response.reason))

    def post_thread(self, forumid, title, body, tag=None, poll=None):
        raise NotImplementedError()

    def find_user_posts(self, user_id):
        raise NotImplementedError()

    def search(self):
        raise NotImplementedError()