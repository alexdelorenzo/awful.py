from bs4 import BeautifulSoup
from sa_tools.base.sa_obj import SAObj
from sa_tools.base.base import Base
from sa_tools.parsers.tools.parser_dispatch import ParserDispatch
from sa_tools.parsers.tools.wrapper import Wrapper, BeauToLxml


class Parser(SAObj, ParserDispatch):
    def __init__(self, *args, wrapper=Wrapper, parser_map: dict=None, **kwargs):
        super().__init__(*args, parser_map=parser_map, **kwargs)
        self.wrapper = wrapper()

    def parse(self, content=None, parent=None, wrapper=BeauToLxml, *args, **kwargs) -> Wrapper:
        if content:
            wrapped_content = self.wrapper.wrap_content(content, wrapper)

            if parent is not None:
                parent._content = wrapped_content

            return wrapped_content

        else:
            return None