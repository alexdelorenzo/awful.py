from SATools.SAThread import SAThread

__author__ = 'alex'

import bs4


class SAForum(object):
	def __init__(self, id, session, name=None):
		self.name = name
		self.base_url = 'http://forums.somethingawful.com/forumdisplay.php'
		self.id = id
		self.session = session

		self.bs_content = None
		self.listings = None
		self.threads = None

	def read(self, pg=1):
		self.listings = self._get_threads(pg)
		self.threads = {id: SAThread(id, self.session, name=name)
		                for id, name in self.listings.items()}


	def _get_threads(self, pg):
		response = self.session.post(self.base_url,
		                        {'forumid': self.id,
		                         'pagenumber': pg})
		content = response.content

		self.bs_content = bs4.BeautifulSoup(content)

		threads = {link['href'].split('=')[-1]: link.text
		           for link in self.bs_content.select('a.thread_title')}

		#self.bs_content = None
		return threads


def main():
	pass


if __name__ == "__main__":
	main()