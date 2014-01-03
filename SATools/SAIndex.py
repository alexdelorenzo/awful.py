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

		#self._get_sections_old()
		#self._get_forums_listing_old()
		self._select_sections()


	def _get_forums_listing_old(self):
		for forum_id, forum_obj in self._gen_forums_old():
			self.forums[forum_id] = forum_obj
			self.listings[forum_id] = forum_obj.name

	def _get_sections_old(self):
		for section_id, section_obj in self._gen_sections_old:
			self.sections[section_id] = section_obj

	def _gen_forums_old(self):
		"""
		TODO: this can be made recursive if attr names had a sane
					naming scheme. lol at a quadruple nested for loop that
					doesn't touch all the sub-sub-subforums
		"""
		for section_id, section_obj in self.sections.items():
			for forum_id, forum_obj in section_obj.subforums.items():
				forum_obj._get_subforums()
				yield forum_id, forum_obj

	def _gen_sections_old(self):
		for category in self.content.select('th.category'):
			category_id = category.a['href'].split('forumid=')[-1]
			name = category.a.text

			category_obj = SAForum(category_id, self.session, name=name)
			category_obj.read()

			yield category_id, category_obj


	def _select_sections(self):
		"""
		TODO: refactor dis
		"""
		forums_table = self.content.find('table', id='forums')

		sections = ordered()

		for section in forums_table.select('tr.section'):
			section_name = section.a.text
			section_id = section.a['href'].split('=')[-1]

			section_subforums = ordered()
			for forum in section.find_next_siblings('tr'):
				nx_class = forum['class'][-1]

				if nx_class == 'section':
					break

				forum_id = nx_class
				forum_name = forum.find('a', 'forum').text

				subforums = ordered()

				for subforum in forum.find('div', 'subforums').find_all('a'):
					subforum_id = subforum['href'].split('forumid=')[-1]
					print(subforum_id)
					subforum_name = subforum.text
					sa_subforum = SAForum(subforum_id, self.session,
					                      subforum_name, subforum_name)

					self.forums[subforum_id] = sa_subforum
					subforums[subforum_id] = sa_subforum
					self.listings[subforum_id] = sa_subforum.name

				sa_forum = SAForum(forum_id, self.session,
				                   forum_name, subforums=subforums)

				self.forums[forum_id] = sa_forum
				section_subforums[forum_id] = sa_forum
				self.listings[forum_id] = sa_forum.name

			self.sections[section_id] = \
				SAForum(section_id, self.session, section_name,
				        subforums=section_subforums)
			self.listings[section_id] = self.sections[section_id].name


def main():
	pass


if __name__ == "__main__":
	main()