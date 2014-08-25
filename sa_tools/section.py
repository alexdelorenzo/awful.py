from sa_tools.base.sa_obj import SAObj


class SASection(SAObj):
    def __init__(self, *args, children: dict=None, **kwargs):
        if children is None:
            children = dict()
        super().__init__(*args, children=children, **kwargs)
        self.children = children
        self.subforums = self.children
        self.forums = self.children
        self._delete_extra()