from sa_tools.base.sa_obj import SAObj
from sa_tools.parsers.reply import ReplyParser


class Reply(SAObj):
    parser = ReplyParser()

    def __init__(self, *args, body: str="", **kwargs):
        super().__init__(*args, **kwargs)

        self.body = body
        self.profile = self.parent.profile

    def reply(self, body: str=None):
        if not body:
            body = self.body

        self.body = body

        return self.parser.reply(body)