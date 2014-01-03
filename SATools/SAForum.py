from SATools.SAThread import SAThread
from collections import OrderedDict as ordered

import bs4
import re
from math import floor


class SAForum(object):
	def __init__(self, id, session, name=None):
		self.name = name
		self.base_url = 'http://forums.somethingawful.com/forumdisplay.php'
		self.id = id
		self.session = session

		self.content = None
		self.listings = None
		self.threads = None
		self.pages = None

	def read(self, pg=1):
		self.threads = self._get_threads()
		self.listings = self.threads


	def _get_threads(self, pg):
		response = self.session.post(self.base_url,
		                        {'forumid': self.id,
		                         'pagenumber': pg})

		self.content = bs4.BeautifulSoup(response.content)

		threads = ordered(self.gen_threads())
		return threads

	def _gen_threads(self):
		thread_blocks = self.content.select('tr.thread')

		for tr_thread in thread_blocks:
			thread_id = tr_thread['id'][6:]
			properties = self._parse_tr_thread(tr_thread)

			key_val = thread_id, \
			     SAThread(thread_id, self.session, properties['title'], properties)

			yield key_val

	def _parse_tr_thread(self, tr_thread):
		properties = dict()

		for td in tr_thread.find_all('td'):
			td_class = td['class'].pop()

			properties[td_class] = td.text.strip()

			if td_class == 'lastpost':
				groups = 'time', 'date', 'user'
				regex = "([0-9]+:[0-9]+) ([A-Za-z 0-9]*, 20[0-9]{2})(.*)"

				matches = re.compile(regex).search(properties[td_class])
				matches = {group: match for group, match in zip(groups, matches)}

				properties[td_class] = matches

			elif td_class == 'replies':
				properties['pages'] = floor(properties[td_class] / 40)

			elif td_class == 'author':
				user_id = td.a['href'].split('id=')[-1]
				properties['user_id'] = user_id

		return properties










def main():
	pass


if __name__ == "__main__":
	main()