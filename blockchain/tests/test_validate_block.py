from django.test import TestCase
from datetime import datetime, timedelta
from blockchain.blockchain_util import *
from blockchain.block import genesis_block


class TestValidateBlock(TestCase):

    def setUp(self):

        # self.block_header = {
        #     'parent_hash': 'test_hash',
        #     'timestamp': datetime.now(),
        #     'beneficiary': 'test_beneficiary',
        #     'difficulty': 1,
        #     'nonce': 'test_nonce',
        #     'number': 1
        # }
        
        
        self.new_block1 = mine(genesis_block['header'], 'beneficiary')
        self.new_block2 = mine(self.new_block1['header'], 'beneficiary')
        
        
      
    def test_parent_block_is_invalid(self):
        
        self.assertFalse(block_is_valid(genesis_block,self.new_block2))
        
    def test_parent_block_is_valid(self):
        
        self.assertTrue(block_is_valid(self.new_block1,self.new_block2))
        
    def test_parent_hash_is_invalid(self):
        
        self.new_block1['header']['parent_hash'] = '000000000'
        
        self.assertFalse(block_is_valid(self.new_block1,self.new_block2))
        
    def test_delta_difficulty_is_invalid(self):
        
        self.new_block2['header']['difficulty'] = 1000
        
        self.assertFalse(block_is_valid(self.new_block1,self.new_block2))
        
        
        