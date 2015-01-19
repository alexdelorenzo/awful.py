from copy import copy
from requests import Session
from sa_tools.base.dynamic import DynamicMixin
from sa_tools.base.magic import MagicMixin
from sa_tools.base.descriptors import IntOrNone

from bs4 import Tag


class SAObj(MagicMixin, DynamicMixin):
    id = IntOrNone()
    _base_url = 'http://forums.somethingawful.com/'

    def __init__(self, parent=None, id: int=None, content: Tag=None, name: str=None, url: str=None, **properties: dict):
        super().__init__(parent, **properties)
        self.id = id
        self.session = None if not self.parent else self.parent.session
        self._content = content
        self.name = name
        self.url = url if url else self._base_url

        self.unread = True
        self._reads = 0

    def _fetch(self, url: str=None, params: dict=None) -> None:
        url = url if url else self. url
        self._content = fetch(self.session, url, params)

    def read(self, pg: int=1) -> None:
        """
        Call _dynamic_attr() and _delete_extra() for full
        sa_obj interop.

        If unread, call them at the end of your overridden read()
        """
        if self.unread:
            self.unread = False

        self._reads += 1

    def _apply_key_vals(self, results, condition_map: dict=None) -> None:
        apply_key_vals(self, results, condition_map)


class SAImmutableObject(SAObj):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _fetch(self, url: str=None, params: dict=None) -> str or bytes:
        url = url if url else self. url
        return fetch(self.session, url, params)

    def read(self, pg: int=1):
        return copy(self)


def fetch(session: Session, url: str, params: dict=None):
    if not params:
        params = dict()

    response = session.get(url, params=params)

    if not response.ok:
        raise Exception(("There was an error with your request ",
                         url, response.status_code, response.reason))

    return response.content


def apply_key_vals(parent, results: iter, condition_map: dict=None) -> None:
    if condition_map is None:
        condition_map = dict()

    for key, val in results:
        if key in condition_map:
            condition_map[key](val)

        else:
            setattr(parent, key, val)