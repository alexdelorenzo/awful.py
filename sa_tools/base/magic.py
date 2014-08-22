from sa_tools.base.base import Base

class MagicMixin(Base):
    def __init__(self, parent: Base=None, *args, **properties):
        super().__init__(parent, *args, **properties)
        self.parent = parent

    def __repr__(self):
        if self.name:
            return self.name

        else:
            return super().__repr__()

    def __str__(self):
        if self.name:
            return self.__repr__()

        else:
            return super().__str__()

    def __getattr__(self, attr):
        """
        Monkey patch of the year, 2014.

        See DynamicMixin._delete_extra for why this exists.
        If I'm not being paid I'm going to have fun.
        """
        is_protected = self._is_protected(attr)

        if is_protected:
            is_magic = self._is_magic(attr)
            is_private = self._is_private(attr)

            lets_not_break_python = is_private or is_magic

            if lets_not_break_python:
                return super().__getattribute__(attr)

        elif attr not in self.__dict__:
            return None

    def __setattr__(self, key, value):
        super().__setattr__(key, value)