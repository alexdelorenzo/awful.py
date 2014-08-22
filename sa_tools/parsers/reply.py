from sa_tools.parsers.parser import Parser

from requests import Response


class ReplyParser(Parser):
    def __init__(self, parent, id=None, reply=None, *args, **kwargs):
        super(ReplyParser, self).__init__(parent, *args, id=id, **kwargs)
        self.body = reply
        self.id = id
        self._base_url = "http://forums.somethingawful.com/newreply.php?action=newreply&"
        self._set_url()

    def reply(self, body: str=None) -> Response:
        inputs = self.parse(body)

        return reply(self.session, self.url, inputs)

    def parse(self, reply: str=None) -> dict:
        super(ReplyParser, self).parse()

        content = fetch(self.session, self.url)
        inputs = parse_inputs(content, reply)

        return inputs

    def _set_url(self, url: str=None):
        if not url:
            url = self._base_url + "&threadid=" + str(self.id)

        self.url = url


def reply(session, url: str, inputs: dict) -> Response:
    response = session.post(url, inputs)

    if not response.ok:
        raise Exception(("Unable to reply", response.status_code, response.reason))

    return response


def fetch(session, url: str) -> str:
    response = session.get(url)
    return response.content


def parse_inputs(content, reply: str) -> dict:
    inputs = {i['name']: i['value']
              for i in content.find_all('input')
              if i.has_attr('value')}

    inputs['message'] = str(reply)
    inputs.pop('preview')

    return inputs

