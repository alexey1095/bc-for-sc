from enum import Enum
from typing import Type
from uuid import uuid4
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from blockchain.blockchain import preprocess_string
from pprint import pprint
from . transaction_types import TransactionType
from state.state import State


# class TransactionType(Enum):

#     CURRENCY_TRANSACTION = 'CURRENCY_TRANSACTION'
#     NEW_ACCOUNT_TRANSACTION = 'NEW_ACCOUNT_TRANSACTION'


class Account:

    def __init__(self, state: Type[State]):

        self.private_key = ec.generate_private_key(ec.SECP256K1())
        self.public_key = self.private_key.public_key()

        #  alias for `public_key` is account address
        self.address = self.public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).hex()

        self.balance = 100000

        self.transaction_pool = {}

        self.state = state

    def generate_signature(self, data):

        result = preprocess_string(data)

        # print('\n generate signature - intermediate steps ')
        # print(f'preprocessed string{data}')
        # print(result)

        signature = self.private_key.sign(result, ec.ECDSA(hashes.SHA256()))

        return signature.hex()

    def signature_is_valid(self, public_key_hex, data, signature):

        result = preprocess_string(data)

        public_key_bytes = bytes.fromhex(public_key_hex)

        public_key_der = serialization.load_der_public_key(public_key_bytes)

        signature_bytes = bytes.fromhex(signature)

        try:
            public_key_der.verify(signature_bytes, result,
                                  ec.ECDSA(hashes.SHA256()))

        except InvalidSignature:
            return False

        return True

    def generate_transaction(self, to, amount=0, data={}):

        # txtx = transact_type.name

        if to:

            transact_type = TransactionType.CURRENCY_TRANSACTION.name

            body = {
                'id': str(uuid4()),
                'type': transact_type,
                'from': self.address,
                'to': to,
                'amount': amount,
                'data': data
            }
            signature = self.generate_signature(body)

            return {
                'body': body,
                'signature': signature
            }

        else:

            transact_type = TransactionType.NEW_ACCOUNT_TRANSACTION.name

            body = {
                'id': str(uuid4()),
                'type': transact_type,
                'address': self.address,
                'balance': self.balance
            }

            return {
                'body': body,
            }

    def currency_transaction_is_valid(self, transaction):

        # from_public_key = transaction['body']['from']

        #  check the balances

        address_from = transaction['body']['from']
        address_to = transaction['body']['to']
        balance_to = self.state._retrieve_account_balance(address_to)

        amount_to_be_sent = transaction['body']['amount']

        if not balance_to:
            print({
                'Error': 'Account `to` is not defined in the state',
                'Address': address_to
            })

            return False

        balance_from = self.state._retrieve_account_balance(address_from)

        if balance_from < amount_to_be_sent:

            print({
                'Error': 'Transaction validation failed - signature is not valid',
                'Details': transaction
            })

            return False

        if not self.signature_is_valid(
            public_key_hex=transaction['body']['from'],
            data=transaction['body'],
            signature=transaction['signature']
        ):
            print({
                'Error': 'Transaction validation failed - signature is not valid',
                'Details': transaction
            })
            return False

        return True

    def add_transaction_to_pool(self, transaction):

        # https://stackoverflow.com/questions/24804453/how-can-i-copy-a-python-string
        transaction_id = (transaction['body']['id']+'.')[:-1]

        transaction_type = transaction['body']['type']

        if transaction_type == TransactionType.CURRENCY_TRANSACTION.name:
            if not self.currency_transaction_is_valid(transaction):
                return False
        # elif transaction_type == TransactionType.NEW_ACCOUNT_TRANSACTION.name:

        self.transaction_pool[transaction_id] = transaction.copy()

        return True

    def return_transaction_pool(self):

        return self.transaction_pool

    def remove_transactions_added_to_block(self, transactions_added_to_block):
        ''' we want to remove those transactions from transaction pool
        that have been added to the block already'''

        print('\n function remove_transactions_added_to_block()')

        pprint(transactions_added_to_block)

        # del self.transaction_pool[t]

        for t in transactions_added_to_block:
            # print('\n inside for loop')
            # pprint(transactions_added_to_block)
            print('print t:' + t)
            if t in self.transaction_pool:
                # del self.transaction_pool[t]
                self.transaction_pool.pop(t)
                print(t)


# if __name__ == "__main__":

#     account = Account()

#     txt = "test message"

#     sig = account.generate_signature(str.encode(txt))

#     print('signature:')
#     print(sig)


#     #  example valid signature
#     res = account.verify_signature(account.address, str.encode(txt), sig)

#     print(res)


#     txt1='ssssss'

#     #  example invalid signature
#     res = account.verify_signature(account.address, str.encode(txt1), sig)

#     print(res)

    # t = account.generate_transaction(
    #     transact_type=TransactionType.CURRENCY_TRANSACTION,
    #     to='somebody',amount=1000,data='test_data')

    # print(t)
