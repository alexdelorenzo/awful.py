from sa_tools.parsers.parser import Parser


class PageNaviParser(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, content) -> int:
        content = super().parse(content)

        return parse_page_selector(content)


def parse_page_selector(content) -> int:
    page_selector = content.find_all('option')

    return int(page_selector[-1].text) if len(page_selector) else 1
