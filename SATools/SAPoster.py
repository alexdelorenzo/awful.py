__author__ = 'alex'

class SAPoster(object):
	def __init__(self, id=None, name=None, session=None, content=None):
		if not id and not content and not name:
			raise TypeError

		self.id = id
		self.name = name
		self.session = session
		self.content = content

		self.avatar_url = None
		self.title = None
		self.reg_date = None
		self.url = None

		if self.id:
			self.url = "https://forums.somethingawful.com/member.php?action=getinfo&userid=" + self.id

		self.read()

	def read(self):
		if self.content:
			if not self.id:
				self.id = self.content.td['class'].pop()
			if self.content.img:
				self.avatar_url = self.content.img['src']
			if not self.name:
				self.name = self.content.find('dt', 'author')

			self.title = self.content.find('dd', 'title')
			self.reg_date = self.content.find('dd', 'registered')
			self.url = "https://forums.somethingawful.com/member.php?action=getinfo&userid=" + self.id

		else:
			pass
			#self._get_profile_from_url()

	def _get_profile_from_url(self):
		raise NotImplementedError



def main():
	pass


if __name__ == "__main__":
	main()