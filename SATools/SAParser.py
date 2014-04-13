from SATools import SAObj
from bs4 import BeautifulSoup, element


class BSWrapper(object):
    def __init__(self, parent, *args, **kwargs):
        super(BSWrapper, self).__init__()
        self.parent = parent
        self._bs_wrappers = BeautifulSoup, element.Tag

    def wrap_parent_content(self):
        content_type = type(self.parent._content)

        if content_type not in self._bs_wrappers:
            self.parent._content = BeautifulSoup(self.parent._content)


class SAParser(SAObj):
    def __init__(self, parent, wrapper, *args, **kwargs):
        super(SAParser, self).__init__(parent, *args, **kwargs)
        self.wrapper = wrapper
        self._delete_extra()

    def parse(self):
        self.read()
        self.wrapper.wrap_parent_content()


class SAForumParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SAForumParser, self).__init__(*args, **kwargs)

    def get_threads(self):
        pass

    def get_subforums(self):
        pass

    def has_subforums(self):
        pass


class SAThreadParser(SAParser):
    def __init__(self, parent, *args, **kwargs):
        super(SAThreadParser, self).__init__(parent, *args, **kwargs)