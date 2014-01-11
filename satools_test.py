__author__ = 'alex'
from AwfulPy import AwfulPy
import unittest


class AwfulPyTest(unittest.TestCase):
	def setUp(self):
		self.ap = AwfulPy('salisbury shake')

	def tearDown(self):
		pass

	def test_read_forum(self):
		self.the_pos = self.ap.index.forums['219']
		self.the_pos.read()

	def test_read_thread(self):
		self.test_read_forum()
		self.thread = self.the_pos.threads['3571697']
		self.thread.read()

	def test_read_post(self):
		self.test_read_thread()
		self.post = self.thread.posts.popitem()[-1]




if __name__ == '__main__':
	unittest.main()
