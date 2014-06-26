class Base(object):
    def __init__(self, parent=None, *args, **kwargs):
        self.parent = parent

    @staticmethod
    def _is_protected(string):
        under = '_'
        first_under = string[0] == under

        return first_under

    @staticmethod
    def _is_magic(string, dunder='__'):
        first_two_dunder = Base._is_protected(string)

        if not first_two_dunder:
            return first_two_dunder

        last_two_dunder = string[-2:] == dunder
        is_magic = first_two_dunder and last_two_dunder

        return is_magic

    @staticmethod
    def _is_private(string, dunder='__'):
        first_two_dunder = string[:2] == dunder

        return first_two_dunder