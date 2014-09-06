from sa_tools.parsers.tools.wrapper import Wrapper
from sa_tools.parsers.parser import Parser


class NaviParser(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, content):
        content = super().parse(content)
        navi_content = content.find('div', 'pages')

        return navi_content


    @staticmethod
    def parse_navi(parent):
        wrapper = Wrapper(parent)
        navi_content = wrapper.content.find('div', 'pages')

        return navi_content