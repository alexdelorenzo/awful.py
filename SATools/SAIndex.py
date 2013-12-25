from SATools.SAForum import SAForum
import bs4

class SAIndex(object):
	def __init__(self, sa_session):
		self.session, self.base_url = sa_session, sa_session.base_url

		self.content = sa_session.get(sa_session.base_url).content
		self.content = bs4.BeautifulSoup(self.content)

		self.listings = self._get_forums_listing(self.content)
		self.forums = [SAForum(id, self.session, name=name) for id, name in self.listings.items()]
		self.forums = {forum.id: forum for forum in self.forums}

		del self.content

	def _get_forums_listing(self, content=None):
		if not content:
			content = self.content

		return {link['href'].split('=')[-1]: link.text for link in content.find_all('a') if 'forumid' in link['href']}





def main():
	pass


if __name__ == "__main__":
	main()