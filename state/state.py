from .trie import Trie
from account.transaction_types import TransactionType


class State():
    ''' The `State` class is used to store and track the state of the system'''

    def __init__(self):

        self.state_trie = Trie()

    def _update_account_balance(self, address, balance):
        ''' update a balance for the existing account 
        or create a new account
        '''
        self.state_trie.store(key=address, value=balance)

    def _retrieve_account_balance(self, address):
        return self.state_trie.retrieve(key=address)

    def get_root_hash(self):
        return self.state_trie.root_hash

    def _process_currency_transaction(self, transaction):
        ''' updates the state of the system by processing the sent currency transaction'''

        from_address = transaction['body']['from']
        to_address = transaction['body']['to']

        #  current balance for the `from` account
        from_balance = self._retrieve_account_balance(from_address)

        #  current balance for the `to` account
        to_balance = self._retrieve_account_balance(to_address)

        amount = transaction['body']['amount']

        from_balance -= amount

        to_balance += amount

        self._update_account_balance(
            address=from_address, balance=from_balance)

        self._update_account_balance(address=to_address, balance=to_balance)

    def _process_new_account_transaction(self, transaction):
        ''' add a new account to the state'''

        self._update_account_balance(
            address=transaction['body']['address'],
            balance=transaction['body']['balance']
        )

    def _process_block_reward_transaction(self, transaction):
        ''' add a new block reward trannsaction to state'''

        beneficiary_address = transaction['body']['to']

        beneficiary_balance = self._retrieve_account_balance(
            beneficiary_address)

        reward = transaction['body']['amount']

        beneficiary_balance += reward

        self._update_account_balance(beneficiary_address, beneficiary_balance)

    def _update_state_new_shipment(self, transaction):
        ''' Update state by adding a new shipment '''

        self.state_trie.store(
            key=transaction['body']['id'],
            value=transaction['body']
        )
        
        
    def _update_state_currency_blocking(self, transaction):
        ''' Update state by adding currency blocking transaction '''
        
        buyer_address = transaction['body']['buyer']

        buyer_balance = self._retrieve_account_balance(
            buyer_address)

        amount_to_block = transaction['body']['amount']

        buyer_balance -= amount_to_block
        
        
        

    def _process_transaction(self, transaction):
        ''' Update the state of the system by processing the sent transaction'''

        # transaction_type = transaction['body']['type']
        transaction_type = transaction['body']['type']

        match transaction_type:

            case TransactionType.CURRENCY_TRANSACTION.name:
                self._process_currency_transaction(transaction)
                return

            case TransactionType.NEW_ACCOUNT_TRANSACTION.name:
                self._process_new_account_transaction(transaction)
                return

            case TransactionType.BLOCK_REWARD_TRANSACTION.name:
                self._process_block_reward_transaction(transaction)
                return

            case TransactionType.CREATE_SHIPMENT_TRANSACTION.name:
                self._update_state_new_shipment(transaction)
                return
            
            case TransactionType.CURRENCY_BLOCKING_TRANSACTION.name:
                self._update_state_currency_blocking(transaction)
                return

            case _:
                raise ValueError(
                    'Error: def process_transaction -- unknown transaction type ' + transaction_type)

    def process_block(self, block):
        ''' update the state by processing the sent block'''

        for id, body in block['transactions'].items():
            self._process_transaction(body)
