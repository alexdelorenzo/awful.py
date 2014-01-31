from bs4 import BeautifulSoup

class SAObj(object):
	def __init__(self, **properties):
		super().__init__()
		self.content = None
		self.session = None
		self.id = None
		self.name = ""
		self.url = ""
		self.base_url = ""
		self.parent = None
		self.unread = True

		for name, attr in properties.items():
			if name in self.__dict__:
				setattr(self, name, attr)

	def read(self, pg=1):
		self.unread = False


class SAListObj(SAObj):
	def __init__(self, **properties):
		super().__init__(**properties)
		self.page = None
		self.pages = None

		self.navi = SAPageNav(parent=self)

		self._collection = []
		self._content = None

	def read(self, pg=1):
		super().read(pg)
		self.navi.read(pg)
		new_url = self.url + '&pagenumber=' + str(pg)
		request = self.session.get(new_url)
		self._content = BeautifulSoup(request.text)

class SAPageNav(SAObj):
	def __init__(self, content=None, parent=None, **properties):
		super().__init__(parent=parent, content=content, **properties)
		self.page = 1
		self.pages = 1

	def read(self, pg=1):
		super().read(pg)

		if not self.content:
			self.content = self.parent.content

		self.page = pg or self.content.find('option', selected='selected').text
		page_selector = self.content.find_all('option')

		if len(page_selector):
			self.pages = page_selector[-1].text
		else:
			self.pages = 1

		self._modify_parent()

	def _modify_parent(self):
		self.parent.page = self.page
		self.parent.pages = self.pages


def main():
	pass


if __name__ == "__main__":
	main()