from SATools.SAForum import SAForum
from SATools.SASection import SASection
from bs4 import BeautifulSoup
from collections import OrderedDict as ordered


class SAIndex(object):
	def __init__(self, sa_session):
		self.session = sa_session
		self.base_url = self.session.base_url

		self.content = BeautifulSoup(self.session.get(self.base_url).content)

		self.sections = ordered()
		self.section_listings = ordered()
		self.forums = ordered()
		self.forum_listings = ordered()
		self.listings = self.forum_listings

		self._select_sections()

	def _save(self, section_id, sa_section):
		self.forums[section_id] = sa_section
		self.listings[section_id] = sa_section.name

	def _select_sections(self):
		forums_table = self.content.find('table', id='forums')
		self.sections = \
			ordered(self._gen_sections(forums_table.select('tr.section')))

	def _gen_sections(self, forums_iter):
		for section in forums_iter:
			section_name = section.a.text
			section_id = section.a['href'].split('=')[-1]

			section_subforums = ordered(self._gen_forum(
																	section.find_next_siblings('tr')))

			sa_section = SASection(section_id, self.session, section_name,
                             subforums=section_subforums, parent=self)

			self._save(section_id, sa_section)
			yield section_id, sa_section

	def _gen_forum(self, section_iter):
		for forum in section_iter:
			nx_class = forum['class'][-1]

			if nx_class == 'section':
				break

			forum_id = nx_class[6:]
			forum_name = forum.find('a', 'forum').text

			div_subforums = forum.find('div', 'subforums').find_all('a')
			subforums = ordered(self._gen_subforum(div_subforums))

			sa_forum = SAForum(forum_id, self.session,
			                   forum_name, subforums=subforums)

			self._save(forum_id, sa_forum)
			yield forum_id, sa_forum

	def _gen_subforum(self, forum_iter):
		for subforum in forum_iter:
			subforum_id = subforum['href'].split('forumid=')[-1]
			subforum_name = subforum.text
			sa_subforum = SAForum(subforum_id, self.session,
			                      subforum_name, subforum_name)

			self._save(subforum_id, sa_subforum)
			yield subforum_id, sa_subforum


def main():
	pass


if __name__ == "__main__":
	main()