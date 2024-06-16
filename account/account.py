from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from blockchain.blockchain import preprocess_string


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

    def verify_signature(self, public_key_hex, data, signature):
        
        result = preprocess_string(data)

        public_key_bytes = bytes.fromhex(public_key_hex)

        public_key_der = serialization.load_der_public_key(public_key_bytes)

        try:
            public_key_der.verify(signature, result, ec.ECDSA(hashes.SHA256()))

        except InvalidSignature:
            return False

        return True


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

   