from sa_tools.parsers.parser import Parser
from sa_tools.search.search_result import SASearchResult


class SearchParser(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self):
        self.wrap()
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