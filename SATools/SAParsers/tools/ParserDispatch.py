from SATools.base.SABase import SABase


class ParserDispatch(SABase):
    def __init__(self, parent, parser_map=None, **kwargs):
        super(ParserDispatch, self).__init__(parent, **kwargs)
        self.parser_map = None
        self.set_parser_map(parser_map)

    def set_parser_map(self, parser_map=None):
        if parser_map is None:
            parser_map = dict()

        self.parser_map = parser_map

    def dispatch(self, key, val=None, content=None):
        if key not in self.parser_map:
            return

        self.parser_map[key](key, val, content)