from SATools.SAThread import SAThread
from collections import OrderedDict as ordered
from math import ceil

import bs4
import re


class SAForum(object):
	def __init__(self, id, session, name=None, subforums=dict(),
	             parent=None,pg=1):
		self.name = name
		self.id = id
		self.session = session
		self.subforums = subforums
		self.parent = parent

		self.base_url = \
			'http://forums.somethingawful.com/forumdisplay.php'

		self.content = None
		self.listings = None
		self.pages = None
		self.page = 1

		self.unread = True

	def read(self, pg=1):
		self.threads = self._get_threads(pg)
		self.listings = {threadid: thread.name
		                 for threadid, thread in self.threads.items()}

		if not self.subforums and self._has_subforums():
			self.subforums = ordered(self._get_subforums())

		self.page = pg or self.content.find('option', selected='selected').text
		page_selector = self.content.find_all('option')

		if len(page_selector):
			self.pages = page_selector[-1].text
		else:
			self.pages = 1

	def _has_subforums(self):
		return self.content.table['id'] == 'subforums'

	def _get_subforums(self):
		for tr_subforum in self.content.select('tr.subforum'):
			subforum_id = tr_subforum.a['href'].split("forumid=")[-1]
			name = tr_subforum.a.text

			forum_obj = SAForum(subforum_id, self.session, name, parent=self)

			yield subforum_id, forum_obj


	def _get_threads(self, pg):
		response = self.session.post(self.base_url,
		                        {'forumid': self.id,
		                         'pagenumber': pg})

		self.content = bs4.BeautifulSoup(response.content)
		self.content = self.content.find('div', id='content')
		threads = ordered(self._gen_threads())

		self.page = pg

		return threads

	def _gen_threads(self):
		thread_blocks = self.content.select('tr.thread')

		for tr_thread in thread_blocks:
			thread_id = tr_thread['id'][6:]
			val = SAThread(id=thread_id, session=self.session, tr_thread=tr_thread)
			key = thread_id
			yield key, val