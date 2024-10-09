from django.test import TestCase



class Test(TestCase):

    def test_example_success(self):
        self.assertTrue(True)

class YetAnotherTest(TestCase):

    def test_example_fails(self):
        self.assertTrue(False)