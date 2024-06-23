from django.test import TestCase
from state.trie import Trie


class TestValidateBlock(TestCase):

    def setUp(self):

        self.trie = Trie()

        self.trie.store('animal', 'cat')
        self.trie.store('fish', 'cod')

    def test_trie_retrieved_correct_values(self):

        self.assertEqual(self.trie.retrieve('animal'), 'cat')
        self.assertEqual(self.trie.retrieve('fish'), 'cod')

    def test_trie_returns_valid_none_value(self):
        self.assertEqual(self.trie.retrieve('wrong_key'), None)

    def test_trie_has_valid_root_hash(self):
        self.assertEqual(
            self.trie.root_hash, "0x6b3b60d989ceebbff5c723ccf9c80311acc815389a50fc61a1ddf7365ed0e636")
        
        
    def test_trie_returns_hard_copy_of_trie(self):
        
        key = 'apple'
        value = 100
        
        self.trie.store(key,value)
        
        val1 = self.trie.retrieve(key)
        
        value = 200
        
        val2 = self.trie.retrieve(key)
        
        self.assertEqual(val1, val2)
        
        
        
        
        
        
        
