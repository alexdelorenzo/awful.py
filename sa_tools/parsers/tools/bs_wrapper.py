from bs4 import BeautifulSoup, element


class BSWrapper(object):
    def __init__(self, parent, *args, **kwargs):
        super(BSWrapper, self).__init__()
        self.parent = parent
        self._bs_wrappers = BeautifulSoup, element.Tag
        self.wrap_parent_content()

    def wrap_parent_content(self):
        if self.content is None:
            return

        if not self._is_wrapped():
            try:
                self.content = BeautifulSoup(self.content, 'lxml')

            except:
                self.content = BeautifulSoup(self.content)

    def _is_wrapped(self, content=None):
        if not content:
            content = self.content

        content_type = type(content)

        return content_type in self._bs_wrappers

    @property
    def content(self):
        return self.parent._content

    @content.setter
    def content(self, new_val):
        self.parent._content = new_val
        self.wrap_parent_content()
