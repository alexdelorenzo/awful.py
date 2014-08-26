from sa_tools.base.base import Base


class ParserDispatch(Base):
    def __init__(self, *args, parser_map: dict=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.parser_map = None
        self.set_parser_map(parser_map)

    def set_parser_map(self, parser_map: dict=None) -> None:
        return set_parser_map(self, parser_map)

    def dispatch(self, *args, **kwargs):
        return dispatch(self, *args, **kwargs)


def set_parser_map(dispatcher: ParserDispatch, parser_map: dict=None) -> None:
    if parser_map is None:
        parser_map = dict()

    setattr(dispatcher, 'parser_map', parser_map)


def dispatch(dispatcher: ParserDispatch, key, *args, **kwargs):
    if key not in dispatcher.parser_map:
        return None

    return dispatcher.parser_map[key](key, *args, **kwargs)