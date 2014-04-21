from SATools.SAParsers.BSWrapper import BSWrapper
from SATools.SAParsers.SAParser import SAParser


class SANaviParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SANaviParser, self).__init__(*args, **kwargs)

    def parse(self):
        super(SANaviParser, self).parse()

    @staticmethod
    def parse_navi(parent):
        wrapper = BSWrapper(parent)
        navi_content = wrapper.content.find('div', 'pages')

        return navi_content


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
