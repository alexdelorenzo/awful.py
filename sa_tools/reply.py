from sa_tools.base.sa_obj import SAObj
from sa_tools.parsers.reply import ReplyParser


class Reply(SAObj):
    def __init__(self, parent, id, body="", *args, **kwargs):
        super(Reply, self).__init__(parent, *args, id=id, **kwargs)
        self.body = body
        self.profile = self.parent.profile
        self.parser = ReplyParser(self, id=self.id, reply=self.body)

    def reply(self, body: str=None) -> None:
        if not body:
            body = self.body

        self.parser.reply(body)
        self.body = body