from SATools.SAPost import SAPost
from SATools.SAPoster import SAPoster
from SATools.SAObj import SAObj, SAListObj

from collections import OrderedDict as ordered
from bs4 import BeautifulSoup
from math import ceil
import re


class SAThread(SAListObj):
	def __init__(self, tr_thread=None, **properties):
		super().__init__(tr_thread=tr_thread, **properties)
		self.base_url = self.session.base_url + 'showthread.php'
		self.url = self.base_url + '?threadid=' + self.id

		self.content = None
		self.posts = None
		self.pages = None
		self.page = 1

		self._set_properties(self._parse_tr_thread(tr_thread))
		self._set_properties(properties)

	def __str__(self):
		return self.name

	def _set_properties(self, properties):
		for name, attr in properties.items():
			if name == 'user_id':
				name = 'poster'
				attr = SAPoster(attr, properties['author'], self.session)

			setattr(self, name, attr)

	def _get_posts(self):
		posts = ordered(self._parse_posts())
		return posts

	def _parse_posts(self):
		"""TODO: grab more info from content, put it in sa_post module..."""
		gen_posts = ((post['id'], SAPost(post['id'], self.session, post))
                  for post in self.content.select('table.post'))
		return gen_posts

	def _parse_tr_thread(self, tr_thread):
		properties = dict()

		for td in tr_thread.find_all('td'):
			td_class = td['class'].pop()
			text = td.text.strip()

			if td_class == 'icon':
				text = td.a['href'].split('posticon=').pop(-1)

			elif td_class == 'lastpost':
				groups = 'time', 'date', 'user'
				regex = "([0-9]+:[0-9]+) ([A-Za-z 0-9]*, 20[0-9]{2})(.*)"
				matches = re.compile(regex).search(text).groups()
				matches = {group: match for group, match in zip(groups, matches)}

				text = matches

			elif td_class == 'replies':
				properties['pages'] = ceil(int(text) / 40)

			elif td_class == 'author':
				user_id = td.a['href'].split('id=')[-1]
				properties['user_id'] = user_id

			elif td_class == 'title' or td_class == 'title_sticky':
				text = td.find('a', 'thread_title').text
				properties['title'] = text

				last_read = td.find('div', 'lastseen')

				if last_read:
					close_link = last_read.a
					stop_tracking_url = self.session.base_url + close_link['href']
					last_post_link = last_read.find('a', 'count')

					if last_post_link:
						unread_count = last_post_link.text
						last_post_url = self.session.base_url + last_post_link['href']
						properties['last_url'] = last_post_url
						properties['unread_count'] = unread_count
						properties['unread_pages'] = ceil(int(unread_count) / 40)
						properties['last_off'] = stop_tracking_url

			properties[td_class] = text

		return properties

	def read(self, page=1):
		new_url = self.url + '&pagenumber=' + str(page)
		request = self.session.get(new_url)

		self.content = BeautifulSoup(request.content)
		self.posts = self._get_posts()

		self.page = page

