from sa_tools.base.base import Base

# This literally does nothing


class DynamicMixin(Base):
    def __init__(self, parent: Base=None, *args, **properties):
        super().__init__(parent, *args, **properties)
        self.parent = parent

        self._substitutes = dict()
        self._properties = dict()

    def _delete_extra(self, delete_protected=True):
        """
        Second runner up.
        """
        significant_false_vals = False, 0, dict()
        delete_these = list(self.__dict__.items())

        for name, val in delete_these:
            is_falsy = not val
            is_special = val in significant_false_vals
            is_protected = self._is_protected(name)
            is_protected = False if delete_protected else is_protected
            isnt_special = not is_special and not is_protected

            if is_falsy and isnt_special:
                delattr(self, name)