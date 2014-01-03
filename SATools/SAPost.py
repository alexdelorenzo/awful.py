from SATools.SAPoster import SAPoster


class SAPost(object):
	def __init__(self, id, session, content=None):
		self.id = id
		self.content = content
		self.session = session

		user_id = self.content.td['class'][0][7:]
		user_name = self.content.dt.text

		self.poster = SAPoster(user_id, user_name, self.session)

		if content:
			self.body = content.td.next_sibling.next_sibling.text.strip()

	def read(self):
		pass


def main():
	pass


if __name__ == "__main__":
	main()