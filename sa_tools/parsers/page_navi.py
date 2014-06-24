from sa_tools.parsers.parser import Parser



class PageNaviParser(Parser):
    def __init__(self, *args, **kwargs):
        super(PageNaviParser, self).__init__(*args, **kwargs)

    def parse(self):
        super(PageNaviParser, self).parse()
        self._parse_page_selector()

    def _parse_page_selector(self):
        page_selector = self.content.find_all('option')

        if len(page_selector):
            self.parent.pages = page_selector[-1].text
        else:
            self.parent.pages = 1