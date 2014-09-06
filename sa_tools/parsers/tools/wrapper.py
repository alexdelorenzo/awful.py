from functools import lru_cache
from lxml.etree import XPath
from lxml.html import HtmlElement, Element, fromstring
from bs4 import BeautifulSoup, Tag


class BeauToLxml(object):
    def __init__(self, html: None):
        super().__init__()
        html_type = type(html)

        if html_type in (str, bytes):
            self.html = fromstring(html)

        elif html_type == BeauToLxml:
            self.html = html.html

        elif html_type in (Element, HtmlElement):
            self.html = html

        elif html_type in (Tag, BeautifulSoup):
            self.html = fromstring(str(html))

    def __repr__(self):
        return 'BeauToLxml: ' + repr(self.html)

    def __getitem__(self, item):
        items = self.html.attrib[item]

        if item == 'class':
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


def find(html: Element, tag: str, _class: str=None, **kwargs) -> Element or None:
    results = find_all(html, tag, _class, iter=True, **kwargs)

    return next(results) if results else None


def find_all(html: Element, tag: str, _class: str=None, iter=False, **kwargs) -> tuple:
    xpath = get_xpath(tag, _class, **kwargs)
    elems = xpath(html)
    
    if not elems:
        return tuple()
    
    wrapper_imap = map(BeauToLxml, elems)
    
    if iter:
        return wrapper_imap
    
    else:
        return tuple(map(BeauToLxml, wrapper_imap))


@lru_cache(maxsize=None)
def get_xpath(tag: str, _class: str=None, **kwargs) -> XPath:
    tag_xp = './/' + tag

    if _class:
        kwargs['class'] = _class

    for attr, val in kwargs.items():
        tag_xp += '['
        attr_xp = '@' + attr
        val_type = type(val)

        is_collection = val_type in (set, list, tuple)
        is_bool = val_type == bool
        is_str = val_type == str

        if is_bool:
            if val is True:
                tag_xp += attr_xp

            else:
                tag_xp += 'not(' + attr_xp + ')'

        elif is_collection:
            for item in val:
                val_xp = '"' + item + '", '

            val_xp = val_xp[:-2]
            tag_xp += 'contains(' + attr_xp + ', ' + val_xp + ')'

        elif is_str:
            tag_xp += 'contains(' + attr_xp + ', "' + val + '")'

        else:
            tag_xp += attr_xp + "='" + val + "'"

        tag_xp += ']'

    return XPath(tag_xp)


class Wrapper(object):
    def __init__(self, parent=None, *args, **kwargs):
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
    return type(content) in wrappers


