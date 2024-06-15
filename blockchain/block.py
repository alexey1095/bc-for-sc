
from datetime import datetime, timedelta
# class BlockHeader:

#     def __init__(self):
#         self.parent_hash = None
#         #  the date when the block was created
#         self.timestamp = None
#         self.beneficiary = None
#         self.difficulty = None
#         self.nonce = None
#         # represents the position of the block in the chain
#         self.number = None


'''Block header dictionary
    `parent_hash`- cryptographic hash of the parent block
    '''

''''''

# block_header = dict.fromkeys(
#     ['parent_hash', 'timestamp', 'block_number', 'difficulty', 'beneficiary'])


# block = dict.fromkeys(
#     ['block_header', 'nonce', 'transactions'])


genesis_block = {
    'header': {
        'parent_hash': 'na_genesis_block',
        'timestamp': '2024-06-15 20:27:12.440884', #str(datetime.now() -timedelta(seconds=90)),
        'block_number': 0,
        'difficulty': 3,
        'beneficiary': 'na_genesis_block',
        'nonce': 0
        },
    
    'transactions': []
}


# class BlockPOW:
#     def __init__(self, header):
#         self.header = header
#         self.max_hash = int('f'*64, 16)
#         print('max hash : ', self.max_hash)
#         print('max hash hex :' + format(self.max_hash,  '#066x'))


#     def get_keccak_hash(self, data):

#         sorted_data = ''.join(sorted(str(data)))
#         hash_bin = keccak.new(data=sorted_data, digest_bits=256).digest()
#         hash_hex = binascii.hexlify(hash_bin)

#         return hash_hex

#     def get_target_hash(self, parent_difficulty):

#         # https://stackoverflow.com/questions/66930326/convert-int-to-hex-of-a-given-number-of-characters

#         print('parent difficulty: ' + str(parent_difficulty))

#         # https://stackoverflow.com/questions/27946595/how-to-manage-division-of-huge-numbers-in-python

#         # here `#066x` 66 is because 64 hex-digits +2 symbols for 0x
#         return format(self.max_hash // int(parent_difficulty), '#066x')

#     def mine(self, parent_block, beneficiary):

#         target_hash = self.get_target_hash(parent_difficulty)
#         timestamp = datetime.datetime.now()
#         difficulty = parent_difficulty+1 # temp solution
#         number =1

#         tmp_hash = self.get_keccak_hash()
