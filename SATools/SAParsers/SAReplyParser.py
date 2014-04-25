from SATools.SAParsers.SAParser import SAParser


class SAReplyParser(SAParser):
    def __init__(self, *args, id=None, reply=None, **kwargs):
        super(SAReplyParser, self).__init__(*args, id=id, **kwargs)
        self.body = reply
        self.id = id
        self._base_url = "http://forums.somethingawful.com/newreply.php?action=newreply&"

    def reply(self, reply=None):
        self.parse(reply)
        self.body = reply

    def parse(self, reply=None):
        super(SAReplyParser, self).parse()
        self._fetch()
        self._parse_inputs()
        self.reply()

    def _fetch(self, url=None):
        if not url:
            self._set_url()
            url = self.url

        response = self.session.get(url)
        self.content = response.content

    def _set_url(self, url=None):
        if not url:
            url = self._base_url + "&threadid=" + str(self.id)

        self.url = url

    def _reply(self, inputs=None):
        if not inputs:
            inputs = self.inputs

        response = self.session.post(self.url, inputs)

        if not response.ok:
            raise Exception(("Unable to reply", response.status_code, response.reason))


    def _parse_inputs(self, reply=None):
        if not reply:
            reply = self.reply

        inputs = {i['name']: i['value']
                  for i in self.content.find_all('input')
                  if i.has_attr('value')}

        inputs['message'] = str(reply)
        inputs.pop('preview')

        self.inputs = inputs

