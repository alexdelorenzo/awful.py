from SATools.SAForum import SAForum
from bs4 import BeautifulSoup
from collections import OrderedDict as ordered


class SAIndex(object):
	def __init__(self, sa_session):
		self.session, self.base_url = sa_session, sa_session.base_url
		self.content = BeautifulSoup(sa_session.get(sa_session.base_url).content)

		self.sections = ordered()
		self.section_listings = ordered()
		self.forums = ordered()
		self.forum_listings = ordered()
		self.listings = self.forum_listings

		self._select_sections()

	def _select_sections(self):
		forums_table = self.content.find('table', id='forums')
		self.sections = ordered(self._gen_sections(forums_table.select('tr.section')))

	def _gen_sections(self, forums_iter):
		for section in forums_iter:
			section_name = section.a.text
			section_id = section.a['href'].split('=')[-1]

			section_subforums = ordered(self._gen_forum(
																				section.find_next_siblings('tr')))

			sa_section = SAForum(section_id, self.session,
			                                  section_name,
			                                  subforums=section_subforums)

			self.forums[section_id] = sa_section
			self.listings[section_id] = sa_section.name
			yield section_id, sa_section


	def _gen_forum(self, section_iter):
		for forum in section_iter:
			nx_class = forum['class'][-1]

			if nx_class == 'section':
				break

			forum_id = nx_class
			forum_name = forum.find('a', 'forum').text

			subforums = ordered(
				self._gen_subforum(
					forum.find('div', 'subforums').find_all('a')))


			sa_forum = SAForum(forum_id, self.session,
			                   forum_name, subforums=subforums)

			self.forums[forum_id] = sa_forum
			self.listings[forum_id] = sa_forum.name
			yield forum_id, sa_forum

	def _gen_subforum(self, forum_iter):
		for subforum in forum_iter:
			subforum_id = subforum['href'].split('forumid=')[-1]
			subforum_name = subforum.text
			sa_subforum = SAForum(subforum_id, self.session,
			                      subforum_name, subforum_name)

			self.forums[subforum_id] = sa_subforum
			self.listings[subforum_id] = sa_subforum.name
			yield subforum_id, sa_subforum

	def __get_forums_listing_old(self):
		for forum_id, forum_obj in self.__gen_forums_old():
			self.forums[forum_id] = forum_obj
			self.listings[forum_id] = forum_obj.name
			return DeprecationWarning

	def __get_sections_old(self):
		for section_id, section_obj in self.__gen_sections_old:
			self.sections[section_id] = section_obj
			return DeprecationWarning

	def __gen_forums_old(self):
		"""
		TODO: this can be made recursive if attr names had a sane
					naming scheme. lol at a quadruple nested for loop that
					doesn't touch all the sub-sub-subforums
		"""
		for section_id, section_obj in self.sections.items():
			for forum_id, forum_obj in section_obj.subforums.items():
				forum_obj._get_subforums()
				yield DeprecationWarning

	def __gen_sections_old(self):
		for category in self.content.select('th.category'):
			category_id = category.a['href'].split('forumid=')[-1]
			name = category.a.text

			category_obj = SAForum(category_id, self.session, name=name)
			category_obj.read()

			yield DeprecationWarning



def main():
	pass


if __name__ == "__main__":
	main()