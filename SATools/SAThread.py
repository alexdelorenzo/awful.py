from SATools.SAPost import SAPost
from SATools.SAPoster import SAPoster
from collections import OrderedDict as ordered

from bs4 import BeautifulSoup


class SAThread(object):
	def __init__(self, id, session, name=None, **properties):
		self.name = name
		self.id = id
		self.session = session

		self.base_url = self.session.base_url + 'showthread.php'
		self.url = self.base_url + '?threadid=' + self.id

		self.content = None
		self.posts = None
		self.pages = None
		self.page = 1
		self.unread = True

		self._set_properties(properties)

	def __str__(self):
		return self.name

	def _set_properties(self, properties):
		for name, attr in properties.items():
			if name == 'user_id':
				name = 'poster'
				attr = SAPoster(attr, properties['author'], self.session)

			setattr(self, name, attr)

	def _get_posts(self):
		posts = ordered(self._parse_posts())
		return posts

	def _parse_posts(self):
		gen_posts = ((post['id'], SAPost(post['id'], self.session, post))
             for post in self.content.select('table.post'))
		return gen_posts

	def read(self, page=1):
		new_url = self.url + '&pagenumber=' + str(page)
		request = self.session.get(new_url)

		self.content = BeautifulSoup(request.content)
		self.posts = self._get_posts()

		self.page = page




def main():
	pass


if __name__ == "__main__":
	main()