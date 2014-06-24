from unittest import TestCase
from tests.TestObjs.login_details import username, password


class SATest(TestCase):
    @classmethod
    def setUpClass(cls):
        from awful import AwfulPy as AP
        ap = AP(username, password)
        cls.ap = ap