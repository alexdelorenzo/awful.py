from bs4 import BeautifulSoup, Tag
from lxml.html import HtmlElement, Element
from sa_tools import MagicMixin

import lxml


class Wrapper(object):
    def __init__(self, parent, *args, **kwargs):
        super().__init__()

        self.parent = parent

        if self.parent:
            self.wrap_parent_content()

    @staticmethod
    def wrap_content(content: str or bytes or Tag, wrapper=BeautifulSoup) -> BeautifulSoup:
        return wrap_content(content)

    def wrap_parent_content(self, wrapper=BeautifulSoup):
        if self.content is None:
            return

        self.parent._content = wrap_content(self.content, wrapper)

    @property
    def content(self):
        return self.parent._content

    @content.setter
    def content(self, new_val):
        self.parent._content = new_val
        self.wrap_parent_content()


def wrap_content(content: str or bytes or Tag, wrapper=BeautifulSoup) -> BeautifulSoup:
    if not is_wrapped(content):
        try:
            content = wrapper(content, 'lxml')

        except:
            content = wrapper(content)

    return content


def is_wrapped(content: Tag, wrappers: tuple=(BeautifulSoup, Tag)) -> bool:
    content_type = type(content)

    return content_type in wrappers


def find(tag: str, _class: str=None, **kwargs) -> str:
    tag_xp = './/' + tag

    if _class:
        kwargs['class'] = _class

    elif not kwargs:
        return tag_xp

    for attr, val in kwargs.items():
        tag_xp += '['
        attr_xp = '@' + attr
        is_class = attr == 'class'
        is_collection = type(val) in (set, list, tuple)

        if is_class and is_collection:
            for item in val:
                val_xp = '"' + item + '", '

            val_xp = val_xp[:-2]
            tag_xp += 'contains(' + attr_xp + ', ' + val_xp + ')]'

        else:
            tag_xp += attr_xp + "='" + val + "']"

    return tag_xp


class BeauToLxml(MagicMixin):
    def __init__(self, html: str=None):
        html_type = type(html)

        if html_type == str:
            self.html = lxml.html.fromstring(html)

        elif html_type in (Element, HtmlElement):
            self.html = html

        elif html_type in (bytes, Tag, BeautifulSoup):
            self.html = lxml.html.fromstring(str(html))

    def __repr__(self):
        return 'BeauToLxml: ' + repr(self.html)

    def __getitem__(self, item):
        items = self.html.attrib[item]

        if item == 'class':
            items = items.split(' ')

        return items

    def __getattr__(self, item):
        return self.find(item)

    def find(self, tag: str, _class: str=None, **kwargs):
        tag_xp = find(tag, _class, **kwargs)
        print(tag_xp)
        result = self.html.xpath(tag_xp)[0]

        return BeauToLxml(result) if result is not None else None

    def find_all(self, tag: str, _class: str=None, **kwargs) -> list:
        tag_xp = find(tag, _class, **kwargs)

        return list(map(BeauToLxml, self.html.xpath(tag_xp)))

    @property
    def text(self):
        return self.html.text_content()

    def wrap_content(self, content: str or bytes or Tag) -> BeautifulSoup:
        return wrap_content(content, wrapper=self)