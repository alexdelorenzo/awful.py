from SATools.SAObj import SAListObj
from SATools.SASearchResult import SASearchResult
from bs4 import BeautifulSoup

class SASearch(SAListObj):
	def __init__(self, query, type, session, **options):
		super().__init__(session=session, **options)
		self.base_url = "http://forums.somethingawful.com/search.php"
		self.query = query
		self.type = type
		self.results = None

	def read(self, pg=1):
		super().read(pg)

		self._parse_search_results()

		for result in self.results:
			result.read()

	def search_profile(self, sa_profile):
		self.search_userid(sa_profile.id)

	def search_userid(self, user_id):
		search_url = self.base_url + "?action=do_search_posthistory&userid="
		response = self.session.get(search_url + str(user_id))
		response = self._jump(response)

		self._content = BeautifulSoup(response.text)
		self._parse_search_results()

	def _parse_search_results(self):
		table_rows = self._content.find('table', id='main_full').find_all('tr')
		table_header = table_rows.pop(0).find_all('th')
		self._table_header = [th.text.strip() for th in table_header]
		self._table_header.insert(1, 'Snippet')

		self._collection = [SASearchResult(parent=self, content=tr)
		                    for tr in table_rows]
		self.results = self._collection
		self.content = self._content

	def _jump(self, response, base_url=None):
		if not base_url:
			base_url = self.base_url

		bs_content = BeautifulSoup(response.text)
		request_id = bs_content.find('div', 'inner').a['href']
		jump_url = base_url + request_id
		self.url = jump_url

		return self.session.get(jump_url)
