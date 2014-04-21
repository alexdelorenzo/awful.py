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
        is_protected = self._is_protected(attr)

        if is_protected:
            is_magic = self._is_magic(attr)
            lets_not_break_python = is_protected or is_magic

            if lets_not_break_python:
                return super(SAMagic, self).__getattribute__(attr)

        elif attr not in self.__dict__:
            return None

    def __setattr__(self, key, value):
        super(SAMagic, self).__setattr__(key, value)

    def _is_magic(self, string, dunder='__'):
        first_two_dunder = self._is_protected(string)

        if not first_two_dunder:
            return first_two_dunder

        last_two_dunder = string[-2:] == dunder
        is_magic = first_two_dunder and last_two_dunder

        return is_magic

    def _is_protected(self, string, dunder='__'):
        first_two_dunder = string[:2] == dunder

        return first_two_dunder