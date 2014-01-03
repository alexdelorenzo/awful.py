__author__ = 'alex'

class SAPoster(object):
	def __init__(self, id, name, session):
		self.id = id
		self.name = name
		self.session = session

		self.url = "http://forums.somethingawful.com/member.php?action=getinfo&userid=" + self.id


def main():
	pass


if __name__ == "__main__":
	main()