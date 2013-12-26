__author__ = 'alex'
from SATools.SAPoster import SAPoster
import requests
from bs4 import BeautifulSoup
import pickle, os

class SASession(requests.Session):
	def __init__(self, username, passwd):
		super(SASession, self).__init__() #super() args for 2.7 & 3.0+ compat
		self.username = username
		self.base_url = 'https://forums.somethingawful.com/'
		self.login(username, passwd)
		self.id = self.cookies.get('bbuserid')
		self.profile = SAPoster(self.id, username, self)

	def __getstate__(self):
		pickle_this = self.__dict__
		pickle_this['prefetch'], pickle_this['timeout'] = None, None
		return pickle_this

	def login(self, username, passwd):
		login_url = self.base_url + 'account.php'
		post_data = {'username': username, 'password': passwd, 'action': 'login'}

		response = self.post(login_url, post_data)

		if not response.ok:
			raise Exception(("Unable to login", response.status_code, response.reason))


	def post_thread(self, title, body, tag=None, poll=None):
		pass

	def reply(self, id, body):
		url = "http://forums.somethingawful.com/newreply.php?action=newreply&threadid=" + str(id)

		response = self.get(url)
		bs = BeautifulSoup(response.content)

		want = 'action', 'formkey', 'form_cookie'
		inputs = {i['name']: i['value'] for i in bs.find_all('input')
		          if i.has_key('value') and i['name'] in want}
		inputs['parseurl'] = 'yes'
		inputs['message'] = body

		response = self.post(url, inputs)
		return response



def main():
	pass


if __name__ == "__main__":
	main()