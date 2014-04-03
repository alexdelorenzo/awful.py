from SATools import SAObj


class SAParser(SAObj):
    def __init__(self, *args, **kwargs):
        pass


class SAForumParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SAForumParser, self).__init__(*args, **kwargs)
        pass


class SAThreadParser(SAParser):
    def __init__(self, *args, **kwargs):
        super(SAThreadParser, self).__init__(*args, **kwargs)
        pass