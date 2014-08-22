from bs4 import BeautifulSoup, element


class BSWrapper(object):
    def __init__(self, parent, *args, **kwargs):
        super(BSWrapper, self).__init__()
        self.parent = parent
        self._bs_wrappers = BeautifulSoup, element.Tag
        self.wrap_parent_content()

    @staticmethod
    def wrap_content(content):
        return wrap_content(content)

    def wrap_parent_content(self):
        if self.content is None:
            return

        self.parent._content = wrap_content(self.content)

    @property
    def content(self):
        return self.parent._content

    @content.setter
    def content(self, new_val):
        self.parent._content = new_val
        self.wrap_parent_content()


def wrap_content(content) -> BeautifulSoup:
    if not is_wrapped(content):
        try:
            content = BeautifulSoup(content, 'lxml')

        except:
            content = BeautifulSoup(content)

    return content


def is_wrapped(content, wrappers=(BeautifulSoup, element.Tag)):
    content_type = type(content)

    return content_type in wrappers