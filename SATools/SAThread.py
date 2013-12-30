from SATools.SAPost import SAPost
from collections import OrderedDict as ordered
__author__ = 'alex'

from bs4 import BeautifulSoup


class SAThread(object):
	def __init__(self, id, session, name=None):
		self.name = name
		self.id = id
		self.session = session

		self.base_url = session.base_url + 'showthread.php'
		self.url = self.base_url + '?threadid=' + id
		self.content = None
		self.posts = None
		self.pages = None

	def read(self, page=1):
		request = self.session.get(self.url)
		self.content = BeautifulSoup(request.content)
		self.posts = self._get_posts()

	def _get_posts(self):
		gen_posts = ((post['id'], SAPost(post['id'], self.session, post))
		             for post in self.content.select('table.post'))

		posts = ordered(gen_posts)

		return posts



def main():
	pass


if __name__ == "__main__":
	main()