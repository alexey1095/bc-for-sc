from django.test import TestCase
import datetime
from blockchain.blockchain_util import *

# //from .block import BlockPOW

# Create your tests here.


class Foo(TestCase):

    def setUp(self):

        self.block_header = {
            'parent_hash': 'test_hash',
            'timestamp': datetime.datetime.now(),
            'beneficiary': 'test_beneficiary',
            'difficulty': 1,
            'nonce': 'test_nonce',
            'number': 1
        }

        self.genesis_block = {
            'header': {
                'parent_hash': 'na_genesis_block', 'timestamp': 'na_genesis_block',
                'block_number': 0, 'difficulty': 1, 'beneficiary': 'na_genesis_block'
            },
            'nonce': 0,
            'transactions': ['Z', 'X']
        }

        # self.block = BlockPOW(self.block_header)

    # def test_maximum_hash_value(self):

    #     #
    #     result = self.block.getTargetHash(last_difficulty=1)

    #     self.assertEqual(result, format(self.block.max_hash,  '#066x'))

    # def test_minimum_hash_value(self):

    #     #
    #     result = self.block.getTargetHash(last_difficulty=10000)

    #     self.assertEqual(
    #         result, '0x00068db8bac710cb295e9e1b089a027525460aa64c2f837b4a2339c0ebedfa43')

    def test_keccak256_hash(self):
        '''test the keccak256 return correct output with the correct lenght of 256/4=64'''

        res = generate_keccak256_hash(self.genesis_block)

        self.assertEqual(
            res, "0xc6682c2ba345ba6005fffbf480579a403a992dfcb9c5246dc7d13aba256ab619")
        self.assertEqual(len(res), 64+2)

    # def test_preprocess_string1(self):
    #     ''' test that the output string is equal to the expected output'''

    #     res = preprocess_string(self.genesis_block)

    #     self.assertEqual(res, b"'''''''''''''''''''''',,,,,,001::::::::[]"+
    #                      b"________aaaaaaaaaabbbbbbccccccccddeeeeeeeeeeeeee"+
    #                      b"fffggghhhiiiiiiiiikkkklllllmmmnnnnnnnnnnnnnoooooo"+
    #                      b"pprrrrrssssssssssttttttuuyy{{}}"
    #                      )

    def test_preprocess_string2(self):
        ''' test the same output for the same input but differently ordered input'''

        res1 = preprocess_string('{"key1":"val1","key2":"val2"}')
        res2 = preprocess_string('{"key2":"val2","key1":"val1"}')

        self.assertEqual(res1, res2)

    def test_preprocess_string3(self):
        ''' test the output for differently strings'''

        res1 = preprocess_string('{"key1":"val1","key2":"val2"}')
        res2 = preprocess_string('{"key3":"val3","key4":"val4"}')

        self.assertNotEqual(res1, res2)

    def test_generate_target256_hash_returns_max_hash(self):
        ''' tests that the max hash is correctly returned'''

        self.assertEqual(generate_target256_hash(
            parent_difficulty=1), '0x'+'f'*64)

    def test_generate_target256_hash_returns_64_character_hash(self):
        ''' tests the lenght of the hash - should always be 64 + 2 characters'''

        res = generate_target256_hash(parent_difficulty=10000)
        # the `+2` is for `0x`
        self.assertEqual(len(res), 64+2)
        
        
    def test_mine_block(self):
        
        new_block = mine(self.genesis_block['header'], 'beneficiary')
        
        self.assertIs(type(new_block), dict)
