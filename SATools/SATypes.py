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
        super(IntOrNone, self).__init__(value)
        self.value = IntOrNone.int_check(value)

    def __set__(self, instance, value):
        value = IntOrNone.int_check(value)
        super(IntOrNone, self).__set__(instance, value)

    @staticmethod
    def int_check(value):
        try:
            value = int(value)

        except Exception as ex:
            valid_errors = TypeError, ValueError
            is_valid_error = type(ex) in valid_errors

            if is_valid_error:
                if value is not None:
                    value = None

            else:
                raise ex

        return value


class TriggerProperty(WeakRefDescriptor):
    def __init__(self, trigger, name=None, value=None, lim=0):
        super(TriggerProperty, self).__init__(value)
        self.trig_str = trigger
        self.name = name
        self.lim = lim
        self.count = 0

    def __get__(self, instance, owner):
        self.count += 1
        value = super(TriggerProperty, self).__get__(instance, owner)

        is_falsy = not value
        reached_access_lim = self.count >= self.lim
        should_trigger = is_falsy and reached_access_lim

        is_unread = instance.unread is True

        if should_trigger and is_unread:
            callback = getattr(instance, self.trig_str)
            callback()

            value = super(TriggerProperty, self).__get__(instance, owner)

        return value


class ConditionDescriptor(WeakRefDescriptor):
    def __init__(self, value=None, conditional_cb=None):
        super(ConditionDescriptor, self).__init__(value)

        if not conditional_cb:
            conditional_cb = []

        self.conditional_cb = conditional_cb

    def __get__(self, instance, owner):
        pass
