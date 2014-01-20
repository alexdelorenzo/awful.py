__author__ = 'alex'

class SAObj(object):
	def __init__(self, **properties):
		super().__init__()
		self.session = None
		self.id = None
		self.name = ""
		self.url = ""
		self.base_url = ""

		for name, attr in properties.items():
			if name in self.__dict__:
				setattr(self, name, attr)

	def read(self, pg=1):
		raise NotImplementedError


class SAListObj(SAObj):
	def __init__(self, **properties):
		super().__init__(**properties)
		self.content = None
		self.page = None
		self.pages = None
		self.unread = True

		self._collection = []
		self._content = None

def main():
	pass


if __name__ == "__main__":
	main()