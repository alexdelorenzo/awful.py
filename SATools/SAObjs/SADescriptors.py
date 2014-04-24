from weakref import WeakKeyDictionary as wkdict


class WeakRefDescriptor(object):
    def __init__(self, *args, value=None, **kwargs):
        super(WeakRefDescriptor, self).__init__()
        self.value = value
        self.weak_ref = wkdict()
        self.access_count = 0

    def __get__(self, instance, owner):
        self.access_count += 1
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
        """
        I blame jet lag and lack of sleep for this.
        """

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


class TriggerLimit(WeakRefDescriptor):
    def __init__(self, *args, interval=None, **kwargs):
        if interval is None:
            interval = [0, None]

        super(TriggerLimit, self).__init__(*args, **kwargs)
        lower_lim, upper_lim = interval
        self.lower_lim = lower_lim
        self.upper_lim = upper_lim
        
    def _within_limits(self, value, instance):
        count, trig_lim = self.access_count, self.upper_lim
        reached_access_lim = count >= self.lower_lim
        below_trig_lim = count <= trig_lim if trig_lim else True
        within_limits = reached_access_lim and below_trig_lim

        return within_limits


class TriggerProperty(TriggerLimit):
    def __init__(self, trigger, name=None, value=None, *args, **kwargs):
        super(TriggerProperty, self).__init__(value, *args, **kwargs)
        self.trig_str = trigger
        self.name = name

    def __get__(self, instance, owner):
        value = super(TriggerProperty, self).__get__(instance, owner)
        will_trigger = self._will_trigger(value, instance)

        if will_trigger:
            callback = getattr(instance, self.trig_str)
            callback()

            value = super(TriggerProperty, self).__get__(instance, owner)

        return value

    def _will_trigger(self, value, instance):
        is_falsy = not value
        within_limits = self._within_limits(value, instance)
        should_trigger = is_falsy and within_limits
        is_unread = instance.unread is True
        will_trigger = should_trigger and is_unread

        return will_trigger