from sa_tools.parsers.tools.bs_wrapper import BSWrapper
from sa_tools.parsers.parser import Parser



class NaviParser(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self):
        super().parse()

    @staticmethod
    def parse_navi(parent):
        wrapper = BSWrapper(parent)
        navi_content = wrapper.content.find('div', 'pages')

        return navi_content