from sa_tools.base.magic import Base

from re import compile


class RegexManager(Base):
    def __init__(self, parent: Base=None, regex_map: dict=None, regex_strs: dict=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.regex_map = dict()
        self.regex_strs = dict()
        self.set_regex(regex_map, regex_strs)

    def set_regex(self, regex_map: dict=None, regex_strs: dict=None):
        self.set_regex_map(regex_map)
        self.set_regex_strs(regex_strs)

    def set_regex_map(self, regex_map: dict=None) -> None:
        if not regex_map:
            regex_map = dict()

        self.regex_map = regex_map

    def set_regex_strs(self, regex_strs: dict=None) -> None:
        if not regex_strs:
            regex_strs = dict()

        self.regex_strs = regex_strs

    def regex_lookup(self, key: str):
        return regex_lookup(self.regex_map, self.regex_strs, key)

    def regex_matches(self, key: str, string: str) -> dict:
        return regex_matches(self.regex_map, self.regex_strs, key, string)


def regex_lookup(regex_map: dict, regex_strs: dict, key: str):
    exists = key in regex_map

    if exists:
        regex_c = regex_map[key]

    else:
        regex_str = regex_strs[key]
        regex_c = compile(regex_str)
        regex_map[key] = regex_c

    return regex_c


def regex_matches(regex_map: dict, regex_strs: dict, key: str, string: str) -> dict:
    regex_c = regex_lookup(regex_map, regex_strs, key)
    matches = regex_c.search(string).groups()

    return matches