from SATools.SAForum import SAForum
from bs4 import BeautifulSoup
from collections import OrderedDict as ordered

class SAIndex(object):
	def __init__(self, sa_session):
		self.session, self.base_url = sa_session, sa_session.base_url

		self.content = BeautifulSoup(sa_session.get(sa_session.base_url).content)

		self.sections = ordered()
		self.listings = ordered()
		self.forums = ordered()

		self._get_sections()
		self._get_forums_listing()

		print(self.forums)
		print(self.listings)

	def _get_forums_listing(self):
		for forum_id, forum_obj in self._gen_forums():
			self.forums[forum_id] = forum_obj
			self.listings[forum_id] = forum_obj.name

	def _get_sections(self):
		for section_id, section_obj in self._gen_sections():
			self.sections[section_id] = section_obj

	def _gen_forums(self):
		"""
		TODO: this can be made recursive if attr names had a sane
					naming scheme. lol at a quadruple nested for loop that
					doesn't touch all the sub-sub-subforums
		"""
		for section_id, section_obj in self.sections.items():
			for forum_id, forum_obj in section_obj.subforums.items():
				forum_obj._get_subforums()
				yield forum_id, forum_obj

	def _gen_sections(self):


		for category in self.content.select('th.category'):
			category_id = category.a['href'].split('forumid=')[-1]
			name = category.a.text

			category_obj = SAForum(category_id, self.session, name=name)
			category_obj.read()

			yield category_id, category_obj



def main():
	pass


if __name__ == "__main__":
	main()