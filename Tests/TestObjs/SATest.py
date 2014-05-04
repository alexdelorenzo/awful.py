from unittest import TestCase
from Tests.TestObjs.login_details import username, password


class SATest(TestCase):
    @classmethod
    def setUpClass(cls):
        from AwfulPy import AwfulPy as AP
        ap = AP(username, password)
        cls.ap = ap