#  This is a collection of functions

from datetime import datetime
# from dateutil.relativedelta import relativedelta
import pprint

import random


from Crypto.Hash import keccak


MAX_HASH256_VALUE = int('f'*64, 16)

MAX_NONCE_VALUE = 2 ** 128

# https://ethereumclassic.org/blog/2023-03-15-the-ethereum-classic-mining-difficulty-adjustment-explained
IDEAL_BLOCK_TIME_SECONDS = 13


def preprocess_string(string):
    ''' converts the input text into array of symbols, sort it in an alphabetic
    order and replace all white spaces to ensure that there is the same output 
    for the same input even when input is ordered or formatted differently '''

    return ''.join(sorted(str(string).replace(" ", ""))).encode("utf-8")


def generate_keccak256_hash(input_text):
    ''' generates Keccak256 hash'''

    result = preprocess_string(input_text)
    hash_bin = keccak.new(data=result, digest_bits=256)
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

def adjust_difficulty(current_timestamp, parent_timestamp, parent_difficulty):

    time_delta = current_timestamp - parent_timestamp

    if time_delta.total_seconds() < IDEAL_BLOCK_TIME_SECONDS:
        return parent_difficulty + 1

    reduced_difficulty = parent_difficulty - 1

    if reduced_difficulty < 1:
        return 1

    return reduced_difficulty


def _find_new_block_hash(target_hash, parent_hash, new_block_number, parent_timestamp, parent_difficulty, beneficiary):
    ''' finds the hash for a new block which is a requirement for PoW 
    and returns the new block once hash is found'''

    while True:

        current_timestamp = datetime.now()

        # this is a partial new block header (without nonce)
        new_block_header = {
            'parent_hash': parent_hash,
            'timestamp': str(current_timestamp),
            'block_number': new_block_number,
            'difficulty': adjust_difficulty(
                current_timestamp,
                parent_timestamp,
                parent_difficulty
            ),  # parent_header['difficulty'] + 1,  # temp solution
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
            print('\n')
            print(f'---- Block # {new_block_number}')
            print(f'hash {current_hash} < target_hash {target_hash}')
            pprint.pprint(new_block_header)
            pprint.pprint(f'nonce = {nonce}')
            
            print('\n')
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

    parent_timestamp = datetime.fromisoformat(parent_header['timestamp'])

    parent_difficulty = parent_header['difficulty']

    # calculate the next block number
    new_block_number = parent_header['block_number'] + 1

    new_block = _find_new_block_hash(
        target_hash, parent_hash, new_block_number, parent_timestamp, parent_difficulty, beneficiary)

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


def pow_requirement_met(parent_header, child_header):

    # calculate target hash for a given block
    target_hash = generate_target256_hash(parent_header['difficulty'])

    # extracting `nonce` from the child's header
    child_nonce = child_header['nonce']

    #
    reduced_child_header = child_header.copy().pop('nonce')

    #  calculate hash for the 
    reduced_child_hash = generate_keccak256_hash(reduced_child_header)

    _hash = generate_keccak256_hash(reduced_child_hash + str(child_nonce))

    if (_hash > target_hash):
        
        print('\n ======= DEBUG INFO ================')
        print(f'\n**** Block Validation Error:  Block # {
            child_header['block_number']} has failed to meet the PoW requirement'
        )
        
        print('PoW requirement')
        print(f'hash {_hash} > target hash {target_hash}')
        
        print('\n Parent block')
        pprint.pprint(parent_header)
        
        print('\n Child block (failed to meet PoW requirement)')
        pprint.pprint(child_header)
        print('\n ===================================')

        return False

    return True

    #


def child_block_number_correct(parent_block_number, child_block_number):

    if parent_block_number + 1 != child_block_number:

        print(f'**** Block Validation Error:  Block {
            parent_block_number} is not a parent for the block {
                child_block_number}'
        )
        return False

    return True


def child_block_has_correct_parent_hash(parent_header, child_header):

    parent_block_hash = generate_keccak256_hash(parent_header)

    if parent_block_hash != child_header['parent_hash']:

        print(f'**** Block Validation Error:  Block {
            parent_header['block_number']} is not a parent for the block {
                child_header['block_number']}'
        )
        return False

    return True


def delta_difference_equal_one(parent_header, child_header):
    
    # skiping this check if the parent block is genesis block
    if parent_header['block_number'] ==0:
        return True

    delta_difficulty = parent_header['difficulty'] - child_header['difficulty']

    if delta_difficulty != 1 and delta_difficulty != -1:

        print(f'**** Block Validation Error:  Parent block {
            parent_header['block_number']} and child block  {
            child_header['block_number']} have difference in difficulty more than one {delta_difficulty} '
        )
        return False

    return True


def block_is_valid(parent_block, child_block):

    # check if there is a parent -child relationship between blocks
    # the child's block number should be greater the parent's block number by 1
    
    # if parent_block['header']['block_number'] == 0:
        

    if not child_block_number_correct(
        parent_block['header']['block_number'],
        child_block['header']['block_number']
    ):
        return False

    if not child_block_has_correct_parent_hash(
        parent_block['header'],
        child_block['header']
    ):
        return False

    if not delta_difference_equal_one(
        parent_block['header'],
        child_block['header'] 
    ):
        return False

    # check the proof of work requirement

    if not pow_requirement_met(
        parent_block['header'],
        child_block['header']
    ):
        return False

    return True


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

    # generate_keccak256_hash(genesis_block)
    res = preprocess_string(genesis_block)

    print(f"res= {res}")
