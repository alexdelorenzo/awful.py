from weakref import WeakKeyDictionary as wkdict


class WeakRefDescriptor(object):
    def __init__(self, value=None, *args, **kwargs):
        super().__init__()
        self.value = value
        self.weak_ref = wkdict()
        self.access_count = 0

    def __get__(self, instance, owner):
        self.access_count += 1
        return self.weak_ref.get(instance, self.value)

    def __set__(self, instance, value):
        self.weak_ref[instance] = value


class IntOrNone(WeakRefDescriptor):
    def __init__(self, value=None, *args, **kwargs):
        super().__init__(value)
        self.value = IntOrNone.int_check(value)

    def __set__(self, instance, value):
        value = IntOrNone.int_check(value)
        super().__set__(instance, value)

    @staticmethod
    def int_check(value):
        """
        I blame jet lag and lack of sleep for this.
        """

        try:
            value = int(value)

        except (TypeError, ValueError) as error:
            if value is not None:
                value = None

        return value


class TriggerProperty(WeakRefDescriptor):
    def __init__(self, trigger, name=None, value=None, *args, **kwargs):
        super().__init__(value, *args, **kwargs)
        self.trig_str = trigger
        self.name = name

    def __get__(self, instance, owner):
        value = super().__get__(instance, owner)
        will_trigger = self._will_trigger(value, instance)

        if will_trigger:
            callback = getattr(instance, self.trig_str)
            callback()

            value = super().__get__(instance, owner)

        return value

    def _will_trigger(self, value, instance):
        is_falsy = not value
        is_unread = instance.unread is True
        will_trigger = is_falsy and is_unread

        return will_trigger


class IntOrNoneTrigger(TriggerProperty, IntOrNone):
    def __init__(self, trigger=None, initial=None, value=None, name=None, *args, **kwargs):
        pass