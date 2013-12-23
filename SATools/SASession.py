__author__ = 'alex'

import requests


class SASession(requests.Session):
	def __init__(self, username, passwd):
		super().__init__()
		self.username = username
		self.base_url = 'https://forums.somethingawful.com/'
		self.login(username, passwd)


	def login(self, username, passwd):
		login_url = self.base_url + 'account.php'
		post_data = {'username': username, 'password': passwd, 'action': 'login'}


		response = self.post(login_url, post_data)

		if not response.ok:
			raise Exception((response.status_code, response.reason))





def main():
	pass


if __name__ == "__main__":
	main()