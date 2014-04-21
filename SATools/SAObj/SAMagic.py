__author__ = 'alex'


class SAMagic(object):
    def __init__(self, parent, **properties):
        self.parent = parent

    def __repr__(self):
        if self.name:
            return self.name
        else:
            return super(SAMagic, self).__repr__()

    def __str__(self):
        if self.name:
            return self.__repr__()
        else:
            return super(SAMagic, self).__str__()

    def __getattr__(self, attr):
        """
        Monkey patch of the year, 2014.

        See SADynamic._delete_extra for why this exists.
        If I'm not being paid I'm going to have fun.
        """
        if attr not in self.__dict__:
            return None

    def __setattr__(self, key, value):
        super(SAMagic, self).__setattr__(key, value)