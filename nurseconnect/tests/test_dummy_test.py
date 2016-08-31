from django.test import TestCase


class DummyTestCase(TestCase):
    """
    Dummy test to allow Travis tests to pass.
    This test case should be removed when actual
    tests are written
    """

    def setUp(self):
        pass

    def test_dummy_for_travis(self):
        pass
