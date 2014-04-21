from bs4 import BeautifulSoup, element
from SATools.SAObj.SAMagic import SAMagic
from SATools.SAObj.SAObj import SAObj

from re import compile


class BSWrapper(object):
    def __init__(self, parent, *args, **kwargs):
        super(BSWrapper, self).__init__()
        self.parent = parent
        self._bs_wrappers = BeautifulSoup, element.Tag

    def wrap_parent_content(self):
        if self.content is None:
            return

        if not self._is_wrapped():
            self.content = BeautifulSoup(self.content)

    def _is_wrapped(self, content=None):
        if not content:
            content = self.content

        content_type = type(content)

        if content_type in self._bs_wrappers:
            return True

        else:
            return False

    @property
    def content(self):
        return self.parent._content

    @content.setter
    def content(self, new_val):
        self.parent._content = new_val
        self.wrap_parent_content()


class RegexManagement(SAMagic):
    def __init__(self, *args, regex_map=None, regex_strs=None, **kwargs):
        super(RegexManagement, self).__init__(*args, **kwargs)
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


class SAParser(SAObj):
    def __init__(self, parent, wrapper=BSWrapper, parser_map=None, *args, **kwargs):
        super(SAParser, self).__init__(parent, *args, **kwargs)
        self.id = self.parent.id
        self.wrapper = None
        self._parser_map = None

        self.set_wrapper(wrapper)
        self.set_parser_map(parser_map)
        self._delete_extra()

    def set_wrapper(self, wrapper=BSWrapper):
        self.wrapper = BSWrapper(self.parent)

        if self.parent._content:
            self.wrapper.wrap_parent_content()

    def set_parser_map(self, parser_map=None):
        if parser_map is None:
            parser_map = dict()

        self._parser_map = parser_map

    def dispatch(self, key, val=None, content=None):
        if key not in self._parser_map:
            return

        self._parser_map[key](key, val, content)

    def parse(self):
        self.read()
        self.wrapper.wrap_parent_content()

    @property
    def content(self):
        return self.wrapper.content

    @content.setter
    def content(self, new_val):
        self.wrapper.content = new_val