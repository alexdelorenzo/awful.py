from SATools.SAForum import SAForum
import bs4
from collections import OrderedDict as ordered

class SAIndex(object):
	def __init__(self, sa_session):
		self.session, self.base_url = sa_session, sa_session.base_url

		self.content = sa_session.get(sa_session.base_url).content
		self.content = bs4.BeautifulSoup(self.content)

		self.listings = self._get_forums_listing(self.content)
		self.forums = [SAForum(id, self.session, name=name) for id, name in self.listings.items()]
		self.forums = ordered((forum.id, forum) for forum in self.forums)

		del self.content

	def _get_forums_listing(self, content=None):
		if not content:
			content = self.content

		gen_listings = ((link['href'].split('=')[-1], link.text)
		                for link in content.find_all('a')
		                if 'forumid' in link['href'])

		return ordered(gen_listings)





def main():
	pass


if __name__ == "__main__":
	main()