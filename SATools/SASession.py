from SATools.SAPoster import SAPoster
from SATools.SASearch import SASearch
import requests
from bs4 import BeautifulSoup

class SASession(object):
  def __init__(self, username, passwd):
    super(SASession, self).__init__() #super() args for 2.7 & 3.0+ compat
    self.session = requests.Session()
    self.username = username
    self.base_url = 'https://forums.somethingawful.com/'
    self.login(username, passwd)
    self.id = self.session.cookies.get('bbuserid')
    self.profile = SAPoster(self, self.id, username)

  def __getstate__(self):
    """
    Friends don't let friends use inheritance. Something in the hierarchy is
      overriding the sane behavior which lets us pickle easily. This fixes that.
    """
    pickle_this = self.__dict__
    #pickle_this['prefetch'], pickle_this['timeout'] = None, None
    return pickle_this

  def login(self, username, passwd):
    login_url = self.base_url + 'account.php'
    post_data = {'username': username, 'password': passwd, 'action': 'login'}

    response = self.session.post(login_url, post_data)

    if not response.ok:
      raise Exception(("Unable to login", response.status_code, response.reason))


  def post_thread(self, forumid, title, body, tag=None, poll=None):
    raise NotImplementedError()

  def reply(self, id, body):
    url = "http://forums.somethingawful.com/newreply.php?action=newreply&threadid=" + str(id)

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

  def find_user_posts(self, user_id):
    search = SASearch(query=user_id, session=self.session)
    search.search_userid(user_id)
    return search

  def search(self):
    raise NotImplementedError()