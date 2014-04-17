from weakref import WeakKeyDictionary as wkdict


class WeakRefDescriptor(object):
    def __init__(self, value=None):
        super(WeakRefDescriptor, self).__init__()
        self.value = value
        self.weak_ref = wkdict()

    def __get__(self, instance, owner):
        return self.weak_ref.get(instance, self.value)

    def __set__(self, instance, value):
        self.weak_ref[instance] = value


class IntOrNone(WeakRefDescriptor):
    def __init__(self, value=None):
        super(IntOrNone, self).__init__()
        self.value = IntOrNone._int_check(value)


    def __set__(self, instance, value):
        value = IntOrNone._int_check(value)
        super(IntOrNone, self).__set__(instance, value)

    @staticmethod
    def _int_check(value):
        try:
            value = int(value)

        except Exception as ex:
            valid_errors = TypeError, ValueError

            if type(ex) in valid_errors:
                if value is not None:
                    value = None
            else:
                raise ex

        return value


class ConditionDescriptor(WeakRefDescriptor):
    def __init__(self, value=None, conditional_cb=None):
        super(ConditionDescriptor, self).__init__(value)

        if not conditional_cb:
            conditional_cb = []

        self.conditional_cb = conditional_cb

    def __get__(self, instance, owner):
        pass
