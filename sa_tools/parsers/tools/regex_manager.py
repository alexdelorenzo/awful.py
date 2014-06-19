from sa_tools.base.magic import SABase

from re import compile


class RegexManager(SABase):
    def __init__(self, parent, regex_map=None, regex_strs=None, *args, **kwargs):
        super(RegexManager, self).__init__(parent, *args, **kwargs)
        self.regex_map = dict()
        self.regex_strs = dict()
        self.set_regex(regex_map, regex_strs)

    def set_regex(self, regex_map=None, regex_strs=None):
        self.set_regex_map(regex_map)
        self.set_regex_strs(regex_strs)

    def set_regex_map(self, regex_map=None):
        if not regex_map:
            regex_map = dict()

        self.regex_map = regex_map

    def set_regex_strs(self, regex_strs=None):
        if not regex_strs:
            regex_strs = dict()

        self.regex_strs = regex_strs

    def regex_lookup(self, key):
        exists = key in self.regex_map

        if exists:
            regex_c = self.regex_map[key]

        else:
            regex_str = self.regex_strs[key]
            regex_c = compile(regex_str)
            self.regex_map[key] = regex_c

        return regex_c

    def regex_matches(self, key, string):
        regex_c = self.regex_lookup(key)
        matches = regex_c.search(string).groups()

        return matches