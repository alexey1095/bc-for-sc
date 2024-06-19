from django.test import TestCase
from pprint import pprint
from account.account import Account, TransactionType


class AccountTests(TestCase):

    def setUp(self):
        
        self.account = Account()
        self.message = {'key1':'val1','key2':'val2' }
        
        self.message_different_formating = {'key2':'val2','key1':'val1'}

        
      
    def test_verify_valid_signature(self):
        
        sig = self.account.generate_signature(self.message)
        
        res = self.account.signature_is_valid(self.account.address, self.message, sig)
        
        self.assertEqual(res, True)
        
        
    def test_verify_invalid_signature(self):
        
        sig = self.account.generate_signature(self.message)
        
        invalid_message = 'invalid_message'
        
        res = self.account.signature_is_valid(self.account.address, invalid_message, sig)
        
        self.assertEqual(res, False)
        
        
    def test_generate_currency_transacion(self):
        
        t = self.account.generate_transaction(
            to='some_address',
            amount=1000,data='test_data')
    
    
        pprint(t)
        
        
    def test_generate_account_transacion(self):
        
        t = self.account.generate_transaction(
            to='some_address',
            amount=1000)
    
    
        pprint(t)
        
        
    def test_verify_valid_currency_transacion(self):
        
        t = self.account.generate_transaction(
            to='some_address',
            amount=1000)
        
        status = self.account.currency_transaction_is_valid(t)
        
        self.assertEqual(status, True)
        
        
    def test_verify_invalid_currency_transacion(self):
        
        t = self.account.generate_transaction(
            to='some_address',
            amount=1000)
        
        #  re-write one of the field `amount` of the transaction with
        # a wrong data
        t['body']['amount'] = 10
        
        status = self.account.currency_transaction_is_valid(t)
        
        self.assertEqual(status, False)
        
        
    def test_add_currency_transaction_to_pool(self):
        
        t = self.account.generate_transaction(
            to="some_address",
            amount=1000)
        
        self.account.add_transaction_to_pool(t)
        
        print('Transaction pool')
        
        pprint(self.account.transaction_pool)
        
        
        self.assertEqual(len(self.account.transaction_pool), 1)
        
        
    def test_add_account_transaction_to_pool(self):
        
        t = self.account.generate_transaction(
            to = 'some_address',            
            amount=1000)
        
        self.account.add_transaction_to_pool(t)
        
        print('Transaction pool')
        
        pprint(self.account.transaction_pool)
        
        
        self.assertEqual(len(self.account.transaction_pool), 1)
        
    
    
#  -------------------------------------------------------------------------------
        
        
    # def test_verify_valid_signature_for_same_date_with_different_formatting(self):
        
    #     sig1 = self.account.generate_signature(self.message)
        
    #     sig2 = self.account.generate_signature(self.message_different_formating)
           
        
    #     self.assertEqual(sig1, sig2)
        
        