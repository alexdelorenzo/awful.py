from abc import ABC, abstractmethod
from functools import lru_cache
from lxml.html import HtmlElement, Element, fromstring, tostring
from bs4 import BeautifulSoup, Tag


class BS4Adaoter(ABC):
    @abstractmethod
    def __getitem__(self, item):
        raise NotImplementedError()

    @abstractmethod
    def __getattr__(self, item):
        raise NotImplementedError()

    @abstractmethod
    def find(self, tag: str, _class: str=None, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def find_all(self, tag: str, _class: str=None, **kwargs) -> list:
        raise NotImplementedError()

    @abstractmethod
    @property
    def text(self):
        raise NotImplementedError()


class BeauToLxml(BS4Adaoter):
    def __init__(self, html: None):
        super().__init__()

        if isinstance(html, (str, bytes)):
            self.html = fromstring(html)

        elif isinstance(html, BeauToLxml):
            self.html = html.html

        elif isinstance(html, HtmlElement):
            self.html = html

        elif str(type(html)) in ('Tag', 'BeautifulSoup'):
            self.html = fromstring(str(html))

    def __repr__(self):
        return 'BeauToLxml: ' + repr(self.html)

    def __getitem__(self, item):
        items = self.html.attrib[item]

        if item == 'class' and ' ' in items:
            items = items.split(' ')

        return items

    def __getattr__(self, item):
        return self.find(item)
        # val = self.find(item)
        #
        # if val:
        #     return val
        #
        # else:
        #     return getattr(self.html, item)

    def find(self, tag: str, _class: str=None, **kwargs):
        return find(self.html, tag, _class, **kwargs)

    def find_all(self, tag: str, _class: str=None, **kwargs) -> list:
        return find_all(self.html, tag, _class, **kwargs)

    @property
    def text(self):
        return self.html.text_content()

    @property
    def raw_html(self):
        return tostring(self.html)


def find(html: Element, tag: str, _class: str=None, **kwargs) -> Element or None:
    tag_xp = get_xpath(tag, _class, **kwargs)
    results = html.xpath(tag_xp)

    if results:
        result = html.xpath(tag_xp)[0]

        return None if result is None else BeauToLxml(result)

    else:
        return None


def find_all(html: Element, tag: str, _class: str=None, **kwargs) -> tuple:
    tag_xp = get_xpath(tag, _class, **kwargs)

    return tuple(map(BeauToLxml, html.xpath(tag_xp)))


class Wrapper(object):
    def __init__(self, parent, *args, **kwargs):
        super().__init__()

        self.parent = parent

        if self.parent:
            self.wrap_parent_content()

    @staticmethod
    def wrap_content(content: str or bytes or Tag, wrapper=BeauToLxml) -> BeautifulSoup:
        return wrap_content(content, wrapper=wrapper)

    def wrap_parent_content(self, wrapper=BeauToLxml):
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


def wrap_content(content: str or bytes or Tag, wrapper=BeauToLxml) -> BeautifulSoup:
    if not is_wrapped(content):
        if wrapper == BeautifulSoup:
            try:
                content = wrapper(content, 'lxml')

            except:
                content = wrapper(content)

        else:
            content = wrapper(content)

    return content


def is_wrapped(content: Tag, wrappers: tuple=(BeautifulSoup, Tag, BeauToLxml)) -> bool:
    content_type = type(content)

    return content_type in wrappers


@lru_cache(maxsize=None)
def get_xpath(tag: str, _class: str=None, **kwargs) -> str:
    tag_xp = './/' + tag

    if _class:
        kwargs['class'] = _class

    elif not kwargs:
        return tag_xp

    for attr, val in kwargs.items():
        tag_xp += '['
        attr_xp = '@' + attr

        if isinstance(val, bool):
            if val is True:
                tag_xp += attr_xp + ']'

            else:
                tag_xp += 'not(' + attr_xp + ')]'

        elif isinstance(val, (set, list, tuple)):
            for item in val:
                val_xp = '"' + item + '", '

            val_xp = val_xp[:-2]
            tag_xp += 'contains(' + attr_xp + ', ' + val_xp + ')]'

        elif isinstance(val, str):
            tag_xp += 'contains(' + attr_xp + ', "' + val + '")]'

        else:
            tag_xp += attr_xp + "='" + val + "']"

    return tag_xp