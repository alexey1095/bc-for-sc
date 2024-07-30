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
from shipment.shipment_status import ShipmentStatus


# class TransactionType(Enum):

#     CURRENCY_TRANSACTION = 'CURRENCY_TRANSACTION'
#     NEW_ACCOUNT_TRANSACTION = 'NEW_ACCOUNT_TRANSACTION'


class Account:
    ''' Account class defines key attributes and methods '''

    def __init__(self, state: Type[State]):

        self.private_key = ec.generate_private_key(
            ec.SECP256K1())
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

    # def generate_transaction(self, to, amount=0, data={}):

    #     # txtx = transact_type.name

    #     if to:

    #         transact_type = TransactionType.CURRENCY_TRANSACTION.name

    #         body = {
    #             'id': str(uuid4()),
    #             'type': transact_type,
    #             'from': self.address,
    #             'to': to,
    #             'amount': amount,
    #             'data': data
    #         }
    #         signature = self.generate_signature(body)

    #         return {
    #             'body': body,
    #             'signature': signature
    #         }

    #     else:

    #         transact_type = TransactionType.NEW_ACCOUNT_TRANSACTION.name

    #         body = {
    #             'id': str(uuid4()),
    #             'type': transact_type,
    #             'address': self.address,
    #             'balance': self.balance
    #         }

    #         return {
    #             'body': body,
    #         }

    def generate_currency_transaction(self, to, amount, data=None):
        ''' Generate a currency transaction '''

        if data is None:
            data = {}

        body = {
            'id': str(uuid4()),
            'type': TransactionType.CURRENCY_TRANSACTION.name,
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

    def generate_currency_blocking_transaction(self, amount, ref_txn_id):
        ''' Generate a blocking transaction - this is called by the buyer therefore the 
        '''
        body = {
            'id': str(uuid4()),
            'type': TransactionType.CURRENCY_BLOCKING_TRANSACTION.name,
            'buyer': self.address,
            'amount': amount,
            'ref_txn_id': ref_txn_id
        }
        signature = self.generate_signature(body)

        return {
            'body': body,
            'signature': signature
        }

    def generate_account_transaction(self):
        ''' Generate a transaction to create a new account'''

        body = {
            'id': str(uuid4()),
            'type': TransactionType.NEW_ACCOUNT_TRANSACTION.name,
            'address': self.address,
            'balance': self.balance
        }

        return {
            'body': body,
        }

    # def create_new_shipment(self, vendor, buyer,
    #                         product_description,
    #                         qty,
    #                         price, contract_number):

    #     #  NOTE: this will need to be moved to `api`

    #     # check if both buyer and vendor exit in `state`
    #     buyer_balance = self.state._retrieve_account_balance(buyer)

    #     if not buyer_balance:
    #         print('Error: -- create_new_shipment')
    #         print(f'Buyer does not exist in state - address: {buyer}')
    #         return False

    #     if not self.state._retrieve_account_balance(vendor):
    #         print('Error: -- create_new_shipment')
    #         print(f'Vendor does not exist in state - address: {vendor}')
    #         return False

    #     #  check if `buyer` has enough money
    #     if buyer_balance < price:
    #         print('Error: -- create_new_shipment')
    #         print(f'Buyer does not have enough money to create a new shipemnt - balance: {
    #               buyer_balance} - address: {buyer}')
    #         return False

    #     self._generate_new_shipment_transaction(
    #         vendor=vendor,
    #         buyer=buyer,
    #         product_description=product_description,
    #         qty=qty,
    #         price=price,
    #         contract_number=contract_number
    #     )

    #    if not account.add_transaction_to_pool(tt):
#         return {
#             'Error':'Transaction is not valid',
#             'Details':tt}


#     # tt_encoded = json.dumps(tt)
#     tt_encoded = str(tt)

#     blockchain.redis.publish_transaction(tt_encoded)

        # return True

    def generate_new_shipment_transaction(self, vendor, buyer,
                                          product_description,
                                          qty,
                                          price,
                                          contract_number, previous_shipment):
        ''' Generate a transaction to create a new shipment'''
        
        if previous_shipment == "":
            previous_shipment = 'origin'
        

        body = {
            'id': str(uuid4()),
            'type': TransactionType.CREATE_SHIPMENT_TRANSACTION.name,
            'vendor': vendor,
            'buyer': buyer,
            # 'status': ShipmentStatus.SHIPMENT_CREATED.name,
            'previous_shipment': previous_shipment,
            'data': {
                'product_description': product_description,
                'qty': qty,

                # `price` is the amount that will be deducted from
                # the buyer account and stored in the system until
                #  delivery is confirmed
                'price': price,

                'contract_number': contract_number
            }
        }

        signature = self.generate_signature(body)

        return {
            'body': body,
            'signature': signature
        }

    def generate_confirm_shipment_or_delivery_transaction(self, shipment_id, transaction_type):
        ''' Generate a transaction to confirm an existing shipment'''
        
        if transaction_type == TransactionType.CONFIRM_SHIPMENT_TRANSACTION:
            transaction_type = TransactionType.CONFIRM_SHIPMENT_TRANSACTION.name
        elif transaction_type ==  TransactionType.CONFIRM_DELIVERY_TRANSACTION:
            transaction_type = TransactionType.CONFIRM_DELIVERY_TRANSACTION.name
        else:
            transaction_type = 'wrong_transaction_type'
        
        

        body = {
            'id': str(uuid4()),
            'from': self.address,
            'shipment_id': shipment_id,  # id of the shipment to be confirmed
            'type': transaction_type, #TransactionType.CONFIRM_SHIPMENT_TRANSACTION.name,
            # 'status': ShipmentStatus.SHIPMENT_CONFIRMED.name
        }

        signature = self.generate_signature(body)

        return {
            'body': body,
            'signature': signature
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

    def currency_blocking_transaction_is_valid(self, transaction):

        buyer = transaction['body']['buyer']
        amount = transaction['body']['amount']

        # check if vendor exits in `state` (we do not need to check the buyer because this point is called by buyer)
        buyer_balance = self.state._retrieve_account_balance(buyer)

        if buyer_balance < amount:
            return {
                'ERROR': f'Buyer does not have enough money to create to block  - balance: {
                    buyer_balance} - address: {buyer}'}

        if not self.signature_is_valid(
            public_key_hex=buyer,
            data=transaction['body'],
            signature=transaction['signature']
        ):
            print({
                'Error': 'Transaction validation failed - signature is not valid',
                'Details': transaction
            })
            return False

        return True

    def create_shipment_transaction_is_valid(self, transaction):

        buyer = transaction['body']['buyer']
        vendor = transaction['body']['vendor']
        price = transaction['body']['data']['price']

        # check if vendor exits in `state` (we do not need to check the buyer because this point is called by buyer)
        buyer_balance = self.state._retrieve_account_balance(buyer)

        if not buyer_balance:
            print({'ERROR': f'Buyer does not exist in state - address: {buyer}'})

        if not self.state._retrieve_account_balance(vendor):
            return {'ERROR': f'Vendor does not exist in state - address: {vendor}'}

        if buyer_balance < price:
            return {
                'ERROR': f'Buyer does not have enough money to create a new shipemnt - balance: {
                    buyer_balance} - address: {price}'}

        if not self.signature_is_valid(
            public_key_hex=buyer,
            data=transaction['body'],
            signature=transaction['signature']
        ):
            print({
                'Error': 'Transaction validation failed - signature is not valid',
                'Details': transaction
            })
            return False

        return True

    def confirm_shipment_transaction_is_valid(self, transaction):
        ''' Check if the sent transaction is valid'''

        shipment_id = transaction['body']['shipment_id']
        transaction_sender = transaction['body']['from']
        # transaction_status = transaction['body']['status']

        #  retrive the value for a given shipemnt from trie
        shipment = self.state.retrieve_state_value(shipment_id)

        if not shipment:
            print('\nERROR: Transaction does not exist in state')
            pprint(transaction)
            return False
        
        vendor = shipment['vendor']
        
        if vendor != transaction_sender:
            print({'\nERROR':'Only vendor can confirm the shipment request'})
            pprint(transaction)
            print(f'Transaction sender : {transaction_sender} is not vendor {vendor}')
            return False
        
        
        # if transaction_status != ShipmentStatus.SHIPMENT_CONFIRMED.name:
        #     print({'\nERROR':'Wrong transaction status '})
        #     pprint(transaction)
        #     print(f'Transaction status : {transaction_status} is not  {ShipmentStatus.SHIPMENT_CONFIRMED.name}')
        #     return False
            
        
        
        return True
            
        
    def confirm_delivery_transaction_is_valid(self, transaction):
        
        shipment_id = transaction['body']['shipment_id']
        transaction_sender = transaction['body']['from']
        # transaction_status = transaction['body']['status']

        #  retrive the value for a given shipemnt from trie
        shipment = self.state.retrieve_state_value(shipment_id)

        if not shipment:
            print('\nERROR: Transaction does not exist in state')
            pprint(transaction)
            return False
        
        buyer = shipment['buyer']
        
        if buyer != transaction_sender:
            print({'\nERROR':'Only buyer can confirm the shipment request'})
            pprint(transaction)
            print(f'Transaction sender : {transaction_sender} is not buyer {buyer}')
            return False
        
        
        
        return True
        
        
    def new_account_transaction_is_valid(self, transaction):
        
        
        new_account_address = transaction['body']['address']
        
        #  retrive the value for a given address
        new_account = self.state.retrieve_state_value(new_account_address)

        if new_account:
            print({'\nERROR':'This account address already exists in the system'})
            pprint(transaction)
            return False
        
        return True
        
        

    def add_transaction_to_pool(self, transaction):

        # https://stackoverflow.com/questions/24804453/how-can-i-copy-a-python-string
        transaction_id = (transaction['body']['id']+'.')[:-1]

        transaction_type = transaction['body']['type']

        # if transaction_type == TransactionType.CURRENCY_TRANSACTION.name:
        #     if not self.currency_transaction_is_valid(transaction):
        #         return False
        # # elif transaction_type == TransactionType.NEW_ACCOUNT_TRANSACTION.name:

        match transaction_type:

            case TransactionType.CURRENCY_TRANSACTION.name:
                if not self.currency_transaction_is_valid(transaction):
                    return False

            case TransactionType.CREATE_SHIPMENT_TRANSACTION.name:
                if not self.create_shipment_transaction_is_valid(transaction):
                    return False

            case TransactionType.CONFIRM_SHIPMENT_TRANSACTION.name:
                if not self.confirm_shipment_transaction_is_valid(transaction):
                    return False
                
            case TransactionType.CONFIRM_DELIVERY_TRANSACTION.name:
                if not self.confirm_delivery_transaction_is_valid(transaction):
                    return False

            case TransactionType.CURRENCY_BLOCKING_TRANSACTION.name:
                if not self.currency_blocking_transaction_is_valid(transaction):
                    return False

            case TransactionType.NEW_ACCOUNT_TRANSACTION.name:
                if not self.new_account_transaction_is_valid(transaction):
                    return False

            case _:
                print('Unknown transaction type')
                return False

        #  adding transaction to pool
        self.transaction_pool[transaction_id] = transaction.copy()

        return True

    # def add_create_shipment_txn_to_pool(self, transaction):

    #     # https://stackoverflow.com/questions/24804453/how-can-i-copy-a-python-string
    #     transaction_id = (transaction['body']['id']+'.')[:-1]

    #     transaction_type = transaction['body']['type']

    #     if transaction_type == TransactionType.CURRENCY_TRANSACTION.name:
    #         if not self.currency_transaction_is_valid(transaction):
    #             return False
    #     # elif transaction_type == TransactionType.NEW_ACCOUNT_TRANSACTION.name:

    #     self.transaction_pool[transaction_id] = transaction.copy()

    #     return True

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
