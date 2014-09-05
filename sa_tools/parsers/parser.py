from bs4 import BeautifulSoup
from sa_tools.base.sa_obj import SAObj
from sa_tools.base.base import Base
from sa_tools.parsers.tools.parser_dispatch import ParserDispatch
from sa_tools.parsers.tools.wrapper import Wrapper, BeauToLxml


class Parser(SAObj, ParserDispatch):
    def __init__(self, *args, wrapper=Wrapper, parser_map: dict=None, **kwargs):
        super().__init__(*args, parser_map=parser_map, **kwargs)

        if self.parent:
            self.id = self.parent.id

        self.wrapper = None
        self.set_wrapper(wrapper)

        self.results = dict()
        self._delete_extra()

    def set_wrapper(self, wrapper=Wrapper):
        self.wrapper = wrapper(self.parent)

        if self.parent and self.parent._content:
            self.wrapper.wrap_parent_content(wrapper=BeauToLxml)

    def parse(self, content=None, wrapper=BeauToLxml, *args, **kwargs) -> Wrapper:
        self.read()

        if self.parent:
            self.wrapper.wrap_parent_content(wrapper=wrapper)

        if content:
            return self.wrapper.wrap_content(content, wrapper)


    @property
    def content(self):
        return self.wrapper.content

    @content.setter
    def content(self, new_val):
        self.wrapper.content = new_val


