from SATools.SAObjs.SAObj import SAObj, SAMagic
from SATools.SAParsers.BSWrapper import BSWrapper


class Dispatch(SAMagic):
    def __init__(self, parent, parser_map=None, **kwargs):
        super(Dispatch, self).__init__(parent, **kwargs)
        self._parser_map = None
        self.set_parser_map(parser_map)

    def set_parser_map(self, parser_map=None):
        if parser_map is None:
            parser_map = dict()

        self._parser_map = parser_map

    def dispatch(self, key, val=None, content=None):
        if key not in self._parser_map:
            return

        self._parser_map[key](key, val, content)


class SAParser(SAObj, Dispatch):
    def __init__(self, parent, wrapper=BSWrapper, parser_map=None, *args, **kwargs):
        super(SAParser, self).__init__(parent, *args, **kwargs)
        self.id = self.parent.id
        self.wrapper = None
        self.set_wrapper(wrapper)
        self._delete_extra()

    def set_wrapper(self, wrapper=BSWrapper):
        self.wrapper = wrapper(self.parent)

        if self.parent._content:
            self.wrapper.wrap_parent_content()

    def parse(self):
        self.read()
        self.wrapper.wrap_parent_content()

    @property
    def content(self):
        return self.wrapper.content

    @content.setter
    def content(self, new_val):
        self.wrapper.content = new_val