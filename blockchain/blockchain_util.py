#  This is a collection of functions

import datetime
import random

from Crypto.Hash import keccak


MAX_HASH256_VALUE = int('f'*64, 16)

MAX_NONCE_VALUE = 2 ** 128


def preprocess_string(string):
    ''' converts the input text into array of symbols, sort it in an alphabetic
    order and replace all white spaces to ensure that there is the same output 
    for the same input even when input is ordered or formatted differently '''

    return ''.join(sorted(str(string).replace(" ", ""))).encode("utf-8")


def generate_keccak256_hash(data):
    ''' generates Keccak256 hash'''

    res = preprocess_string(data)
    hash_bin = keccak.new(data=res, digest_bits=256)
    return '0x'+hash_bin.hexdigest()


def generate_target256_hash(parent_difficulty):
    ''' generates the target hash for a block based on the parent block difficulty '''

    # https://stackoverflow.com/questions/66930326/convert-int-to-hex-of-a-given-number-of-characters
    # https://stackoverflow.com/questions/27946595/how-to-manage-division-of-huge-numbers-in-python

    # here `#066x` 66 is because 64 hex-digits +2 symbols for 0x
    return format(MAX_HASH256_VALUE // int(parent_difficulty), '#066x')


# def generate_block_header(parent_hash, timestamp, block_number, difficulty, beneficiary):

#     return {
#         'parent_hash': parent_hash, 'timestamp': timestamp, 'block_number': block_number,
#         'difficulty': difficulty, 'beneficiary': beneficiary
#     }


def _find_new_block_hash(target_hash, parent_hash, new_block_number, parent_header, beneficiary):
    ''' finds the hash for a new block which is a requirement for PoW 
    and returns the new block once hash is found'''

    while True:

        # this is a partial new block header (without nonce)
        new_block_header = {
            'parent_hash': parent_hash,
            'timestamp': str(datetime.datetime.now()),
            'block_number': new_block_number,
            'difficulty': parent_header['difficulty'] + 1,  # temp solution
            'beneficiary': beneficiary
        }

        # generate the hash value for the new block header
        new_header_hash = generate_keccak256_hash(new_block_header)

        # calculate random nonce for PoW
        # See ref. p46 Mastering Ethereum Antonopoulos
        nonce = random.randint(0, MAX_NONCE_VALUE)

        # calcualate the hash value for a given timestamp and given nonce
        current_hash = generate_keccak256_hash(new_header_hash + str(nonce))

        if (current_hash < target_hash):
            break

    # nonce is now added to the `new_block_header`
    new_block_header['nonce'] = nonce

    # return a new block
    return {
        'header': new_block_header,
        'trasactions': []
    }


def mine(parent_header, beneficiary):
    ''' mines a block by spending a CPU power to find a valid block by solving 
    a cryptographic puzzle. Proof of work difficulty determines the rate of 
    how quickly the puzzle can be solved to ensure that the blocks are added 
    at a steady rate. I also protect the blockchain from attackers attempting
    to overtake the network - the attackers can try an create a super long 
    chain in their favor that everyone may be forced to accept , however that
    would require to re-do the proof-of work for the entire block chain - 
    this costs CPU power and money.

    The mining algorithm:
    1. calculate the block target hash: the higher the difficulty - the 
    smaller the target hash value and vice versa
    2. Find a hash which is lower the target hash.
    '''

    # calculate target hash for a given block
    target_hash = generate_target256_hash(parent_header['difficulty'])

    #  calculate hash for the parent block header
    parent_hash = generate_keccak256_hash(parent_header)

    # calculate the next block number
    new_block_number = parent_header['block_number'] + 1

    new_block = _find_new_block_hash(
        target_hash, parent_hash, new_block_number, parent_header, beneficiary)

    return new_block

    # while True:

    #     # this is a partial new block header (without nonce)
    #     new_block_header = {
    #         'parent_hash': parent_hash,
    #         'timestamp': str(datetime.datetime.now()),
    #         'block_number': new_block_number,
    #         'difficulty': parent_header['difficulty'] + 1,  # temp solution
    #         'beneficiary': beneficiary
    #     }

    #     # generate the hash value for the new block header
    #     new_header_hash = generate_keccak256_hash(new_block_header)

    #     # calculate random nonce for PoW
    #     # See ref. p46 Mastering Ethereum Antonopoulos
    #     nonce = random.randint(0, MAX_NONCE_VALUE)

    #     # calcualate the hash value for a given timestamp and given nonce
    #     current_hash = generate_keccak256_hash(new_header_hash + str(nonce))

    #     if (current_hash < target_hash):
    #         break

    # # nonce is now added to the `new_block_header`
    # new_block_header['nonce'] = nonce

    # # return a new block
    # return {
    #     'header': new_block_header,
    #     'trasactions' : []
    #     }

    # pass


if __name__ == "__main__":

    genesis_block = {
    'header': {
        'parent_hash': 'na_genesis_block',
        'timestamp': 'na_genesis_block',
        'block_number': 0,
        'difficulty': 1,
        'beneficiary': 'na_genesis_block'},
    'nonce': 0,
    'transactions': []
}

    res = preprocess_string(genesis_block) #generate_keccak256_hash(genesis_block)

    print(f"res= {res}")
