from sa_tools.base.sa_obj import SAObj
from sa_tools.parsers.reply import SAReplyParser


class SAReply(SAObj):
    def __init__(self, id, body="", *args, **kwargs):
        super(SAReply, self).__init__(*args, id=id, **kwargs)
        self.body = body
        self.profile = self.parent.profile
        self.parser = SAReplyParser(self, id=self.id, reply=self.body)

    def reply(self, body=None):
        if not body:
            body = self.body

        self.parser.reply(body)
        self.body = body