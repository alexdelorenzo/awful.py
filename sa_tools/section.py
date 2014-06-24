from sa_tools.base.sa_obj import SAObj

class SASection(SAObj):
    def __init__(self, parent, id, name=None, children=dict()):
        super(SASection, self).__init__(parent, id, name=name, children=children)
        self.children = children
        self.subforums = self.children
        self.forums = self.children
        self._delete_extra()