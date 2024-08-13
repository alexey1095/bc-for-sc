from django.test import TestCase
from pprint import pprint
from account.account import Account
from blockchain.lib import mine, mine_block
from state.state import State
from blockchain.blockchain import Blockchain
from blockchain.block import genesis_block


class AccountTests(TestCase):

    def setUp(self):
        
        self.state = State()
        self.account = Account(self.state)
        self.message = {'key1': 'val1', 'key2': 'val2'}
       
        self.blockchain = Blockchain(self.account, self.state)

        self.message_different_formating = {'key2': 'val2', 'key1': 'val1'}

        self.account2 = Account(self.state )
        # self.state2 = State()
        # self.blockchain2 = Blockchain(self.account2, self.state2)
        
        
        #  NOTE:  here we are using one local blockchain with two accounts -
        #  this is to avoid the need for blockchain synchronization

        # new_account_transaction = self.account.generate_transaction(to=None)
        # new_account2_transaction = self.account2.generate_transaction(to=None)
        
        new_account_transaction = self.account.generate_account_transaction()
        new_account2_transaction = self.account2.generate_account_transaction()

        self.account.add_transaction_to_pool(new_account_transaction)
        self.account.add_transaction_to_pool(new_account2_transaction)

        b = mine_block(self.blockchain, self.account, self.state)

    def test_verify_valid_signature(self):

        sig = self.account.generate_signature(self.message)

        res = self.account.signature_is_valid(
            self.account.address, self.message, sig)

        self.assertEqual(res, True)
        
        

    def test_verify_invalid_signature(self):

        sig = self.account.generate_signature(self.message)

        invalid_message = 'invalid_message'

        res = self.account.signature_is_valid(
            self.account.address, invalid_message, sig)

        self.assertEqual(res, False)

    def test_generate_currency_transacion(self):

            
        t = self.account.generate_currency_transaction(
            to='some_address',
            amount=1000, data='test_data')

        pprint(t)

    def test_generate_account_transacion(self):

        t = self.account.generate_account_transaction()

        pprint(t)

    def test_verify_valid_currency_transacion(self):

             
        t = self.account.generate_currency_transaction(
            to=self.account2.address,
            amount=1000)

        status = self.account.currency_transaction_is_valid(t)

        self.assertEqual(status, True)

    def test_verify_invalid_currency_transacion(self):

        
        t = self.account.generate_currency_transaction(
            to='some_address',
            amount=1000)

        #  re-write one of the field `amount` of the transaction with
        # a wrong data
        t['body']['amount'] = 10

        status = self.account.currency_transaction_is_valid(t)

        self.assertEqual(status, False)

    def test_add_currency_transaction_to_pool(self):

        
        t = self.account.generate_currency_transaction(
            to=self.account2.address,
            amount=1000)


        self.account.add_transaction_to_pool(t)

        print('Transaction pool')

        pprint(self.account.transaction_pool)

        self.assertEqual(len(self.account.transaction_pool), 1)

    def test_add_account_transaction_to_pool(self):

    
        t = self.account.generate_currency_transaction(
            to=self.account2.address,
            amount=1000)

        self.account.add_transaction_to_pool(t)

        print('Transaction pool')

        pprint(self.account.transaction_pool)

        self.assertEqual(len(self.account.transaction_pool), 1)

    def test_balance_is_correctly_updated_as_result_of_transaction(self):
       
     
        t = self.account.generate_currency_transaction(
            to=self.account2.address,
            amount=100)

        self.account.add_transaction_to_pool(t)

        b = mine_block(self.blockchain, self.account, self.state)

        balance_account = self.state._retrieve_account_balance(
            self.account.address)
        balance_account2 = self.state._retrieve_account_balance(
            self.account2.address)
        
        #  100000 -initial amount +100 (block mining for creating account)
        #  -100 (transaction amount) +100 ()
        
        self.assertEqual(balance_account, 100000+100-100+100)
        self.assertEqual(balance_account2, 100100)
        
        
    def test_sending_transaction_to_invalid_account(self):
        
       
        
        t = self.account.generate_currency_transaction(
            to='invalid_address',
            amount=100)

        res = self.account.add_transaction_to_pool(t)
        
        self.assertEqual(res, False)
         
    
    def test_sending_invalid_amount(self):
          
        t = self.account.generate_currency_transaction(
            to=self.account2.address,
            amount=10000000)

        res = self.account.add_transaction_to_pool(t)
        
        self.assertEqual(res, False)
