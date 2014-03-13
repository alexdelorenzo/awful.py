from SATools.SAPoster import SAPoster
from SATools.SAObj import SAObj


class SAPost(SAObj):
	def __init__(self, id, session, content=None, parent=None, **properties):
		super(SAPost, self).__init__(id, session, content, parent, **properties)
		self.unread = True
		self.url = ""

		user_id = self.content.td['class'].pop()[7:]
		user_name = self.content.dt.text

		content = self.content.find('td', 'userinfo')
		self.poster = SAPoster(user_id, self.session, content, name=user_name)

		if self.content:
			has_post = self.content.find('td', 'postbody')
			self.body = has_post.text if has_post else ""
			self.unread = False

	def read(self):
		self.unread = False
		for td in self.content.find_all('td'):
			if td['class'] == 'userinfo':
				for dd in td.find_all('dd'):
					pass
		raise NotImplemented()


def main():
	pass


if __name__ == "__main__":
	main()
