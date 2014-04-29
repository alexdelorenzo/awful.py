from SATools.SAParsers.SAParser import SAParser



class SAPageNaviParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SAPageNaviParser, self).__init__(*args, **kwargs)

    def parse(self):
        super(SAPageNaviParser, self).parse()
        self._parse_page_selector()

    def _parse_page_selector(self):
        page_selector = self.content.find_all('option')

        if len(page_selector):
            self.parent.pages = page_selector[-1].text
        else:
            self.parent.pages = 1