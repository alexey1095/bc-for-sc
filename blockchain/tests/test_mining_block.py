from django.test import TestCase
from datetime import datetime, timedelta
from blockchain.blockchain_util import *
from blockchain.block import genesis_block

# //from .block import BlockPOW

# Create your tests here.


class Foo(TestCase):

    def setUp(self):

        self.block_header = {
            'parent_hash': 'test_hash',
            'timestamp': datetime.now(),
            'beneficiary': 'test_beneficiary',
            'difficulty': 1,
            'nonce': 'test_nonce',
            'number': 1
        }
      
    def test_preprocess_string1(self):
        ''' test that the output string is equal to the expected output'''
        
        
        string = "{'key1':'val1', 'key2':'val2'}"

        res = preprocess_string(string)

        self.assertEqual(res, b"'''''''',1122::aaeekkllvvyy{}")

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

        new_block = mine(genesis_block['header'], 'beneficiary')

        self.assertIs(type(new_block), dict)

    def test_difficulty_always_gt_zero(self):

        parent_timestamp = datetime.now()
        current_timestamp = parent_timestamp + timedelta(seconds=90)

        difficulty = adjust_difficulty(current_timestamp, parent_timestamp, 0)

        self.assertEqual(difficulty, 1)
        
    def test_increase_difficulty_when_duration_lt_ideal_time(self):

        parent_timestamp = datetime.now()
        current_timestamp = parent_timestamp + timedelta(seconds=1)

        difficulty = adjust_difficulty(current_timestamp, parent_timestamp, 1)

        self.assertEqual(difficulty, 2)
        
        
    def test_decrease_difficulty_when_duration_gt_ideal_time(self):

        parent_timestamp = datetime.now()
        current_timestamp = parent_timestamp + timedelta(seconds=90)

        difficulty = adjust_difficulty(current_timestamp, parent_timestamp, 5)

        self.assertEqual(difficulty, 4)
        
    
    
