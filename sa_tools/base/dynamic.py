from sa_tools.base.base import Base

# This literally does nothi

class DynamicMixin(Base):
    def __init__(self, parent, *args, **properties):
        super(DynamicMixin, self).__init__(parent, *args, **properties)
        self.parent = parent

        self._substitutes = dict()
        self._properties = dict()
        self._dynamic_attr()

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

    def _dynamic_attr(self):
        """
        Consolation prize.
        """
        if not self._properties:
            return

        for name, val in self._properties.items():
            if name in self._substitutes:
                name = self._substitutes[name]
            self._dynamic_property_read(name, val)

        #del self._properties

    def _dynamic_property(self, p_obj=None, name=None, fget=None, fset=None, val=None):
        if p_obj is None:
            p_obj = self

        new_name = '_' + name
        setattr(p_obj, new_name, val)

        if not fget:
            fget = lambda self: getattr(p_obj, new_name)

        if not fset:
            fset = lambda self, new_val: setattr(p_obj, new_name, new_val)

        prop_obj = property(fget, fset)
        setattr(p_obj.__class__, name, prop_obj)

    def _dynamic_property_read(self, name, val, condition=None):
        """
        Evidence of an atrophied brain.
        """
        new_name = '_' + name

        def fget(self):
            attr = getattr(self, new_name)
            is_unread = self.unread
            is_none = attr is None

            if is_unread and not attr:
                self.read()
                return getattr(self, new_name)

            return attr

        self._dynamic_property(name, fget=fget, val=val)