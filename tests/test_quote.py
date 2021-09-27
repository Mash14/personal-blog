import unittest
from app.models import Quote

class QuoteTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Quote class
    '''
    def setUp(self):
        self.new_quote = Quote(23,'J.F.Kenedy','never Give up')

    def test_init(self):
        """
        test_init test case to test if the object is initialized properly
        """
        self.assertEqual(self.new_quote.id,23)
        self.assertEqual(self.new_quote.author,'J.F.Kenedy')
        self.assertEqual(self.new_quote.quote,'never Give up')

    def test_instance(self):
        self.assertTrue(isinstance(self.new_quote,Quote))