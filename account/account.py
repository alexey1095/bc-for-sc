from enum import Enum
from uuid import uuid4
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from blockchain.blockchain import preprocess_string


class TransactionType(Enum):

    CURRENCY_TRANSACTION = 'CURRENCY_TRANSACTION'
    NEW_ACCOUNT_TRANSACTION = 'NEW_ACCOUNT_TRANSACTION'


class Account:

    def __init__(self):

        self.private_key = ec.generate_private_key(ec.SECP256K1())
        self.public_key = self.private_key.public_key()

        #  alias for `public_key` is account address
        self.address = self.public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).hex()

        self.balance = 100000

    def generate_signature(self, data):

        result = preprocess_string(data)

        # print('\n generate signature - intermediate steps ')
        # print(f'preprocessed string{data}')
        # print(result)

        signature = self.private_key.sign(result, ec.ECDSA(hashes.SHA256()))

        return signature

    def signature_is_valid(self, public_key_hex, data, signature):

        result = preprocess_string(data)

        public_key_bytes = bytes.fromhex(public_key_hex)

        public_key_der = serialization.load_der_public_key(public_key_bytes)

        try:
            public_key_der.verify(signature, result, ec.ECDSA(hashes.SHA256()))

        except InvalidSignature:
            return False

        return True

    def generate_transaction(self, transact_type, to=None, amount=None, data=None):

        body = {
            'id': str(uuid4()),
            'type': transact_type.name,
            'from': self.address,
            'to': to,
            'amount': amount,
            'data': data
        }

        if transact_type == TransactionType.CURRENCY_TRANSACTION:
            signature = self.generate_signature(body)
        else:
            signature = None

        return {
            'body': body,
            'signature': signature
        }

    def currency_transaction_is_valid(self, transaction):

        # from_public_key = transaction['body']['from']

        if self.signature_is_valid(
            public_key_hex=transaction['body']['from'],
            data=transaction['body'],
            signature=transaction['signature']
        ):
            return True

        return False


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
