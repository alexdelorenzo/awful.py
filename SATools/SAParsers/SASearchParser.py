from SATools.SAParsers.SAParser import SAParser
from SATools.SASearches.SASearchResult import SASearchResult


class SASearchParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SASearchParser, self).__init__(*args, **kwargs)

    def parse(self):
        super(SASearchParser, self).parse()
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