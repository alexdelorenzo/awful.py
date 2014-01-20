from AwfulPy import AwfulPy
import unittest


class AwfulPyTest(unittest.TestCase):
	def setUp(self):
		self.ap = AwfulPy('Your Username')

	def tearDown(self):
		pass

	def add_forum(self):
		self.the_pos = self.ap.index.forums['219']
		self.the_pos.read()

	def add_thread(self):
		self.thread = self.the_pos.threads['3571697']
		self.thread.read()

	def add_post(self):
		self.post = self.thread.posts.popitem()[-1]

	def test_read_forum(self):
		self.add_forum()

	def test_read_thread(self):
		self.add_forum()
		self.add_thread()

	def test_read_post(self):
		self.add_forum()
		self.add_thread()
		self.add_post()




if __name__ == '__main__':
	unittest.main()
