from django.test import TestCase

from account.account import Account


class AccountTests(TestCase):

    def setUp(self):
        
        self.account = Account()
        self.message = {'key1':'val1','key2':'val2' }
        
        self.message_different_formating = {'key2':'val2','key1':'val1'}

        
      
    def test_verify_valid_signature(self):
        
        sig = self.account.generate_signature(self.message)
        
        res = self.account.verify_signature(self.account.address, self.message, sig)
        
        self.assertEqual(res, True)
        
        
    def test_verify_invalid_signature(self):
        
        sig = self.account.generate_signature(self.message)
        
        invalid_message = 'invalid_message'
        
        res = self.account.verify_signature(self.account.address, invalid_message, sig)
        
        self.assertEqual(res, False)
        
        
    # def test_verify_valid_signature_for_same_date_with_different_formatting(self):
        
    #     sig1 = self.account.generate_signature(self.message)
        
    #     sig2 = self.account.generate_signature(self.message_different_formating)
           
        
    #     self.assertEqual(sig1, sig2)
        
        