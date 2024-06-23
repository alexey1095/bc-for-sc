import copy
from blockchain.lib import generate_keccak256_hash


class Trie():

    # https://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python

    def __init__(self):

        #  this is a root node of the trie
        #  which is the only node that does
        #  not store the `value` only child nodes
        self.root = {}

        # generate hash of empty trie
        self.root_hash = generate_keccak256_hash(self.root)

    def store(self, key, value):
        ''' store the sent `key` and `value` in the trie '''

        current_node = self.root

        for child in key:

            #  when `child` does not exist in the `current_node`
            #  we create a new `child`
            if not child in current_node:
                current_node[child] = {}

            # for both cases when child has existed or just been created
            # we make `child` to be a new `current_node`
            current_node = current_node[child]
            
        #  once the we reache the end of the branch
        #  create a key `value` and assign the send value to it
        current_node['value'] = value
        
        #  adopted from here 
        #  https://stackoverflow.com/questions/5105517/deep-copy-of-a-dict-in-python
        self.root = copy.deepcopy(self.root)

        #  generate hash of trie
        self.root_hash = generate_keccak256_hash(self.root)

    def retrieve(self, key):
        ''' retrieve `value` or `None` for sent `key` '''

        current_node = self.root

        for child in key:

            if child in current_node:
                #  when `child` exists make it a new
                #  current node
                current_node = current_node[child]
            else:
                #  return `None` when `key` does not exist
                return None

        return current_node['value']
