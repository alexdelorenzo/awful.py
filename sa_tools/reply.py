from sa_tools.base.sa_obj import SAObj
from sa_tools.parsers.reply import ReplyParser


class Reply(SAObj):
    parser = ReplyParser()

    def __init__(self, parent, id, body="", *args, **kwargs):
        super().__init__(parent, *args, id=id, **kwargs)
        self.body = body
        self.profile = self.parent.profile

    def reply(self, body: str=None) -> None:
        if not body:
            body = self.body

        self.body = body

        return self.parser.reply(body)