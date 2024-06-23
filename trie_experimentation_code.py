from pprint import pprint
from blockchain.lib import generate_keccak256_hash
from state.trie import Trie

if __name__ == '__main__':

    # trie = Trie()

    # print('\n')
    # print(f'root_hash {trie.root_hash}')
    # trie.store('animal', 'cat')
    # print('\n')
    # pprint(trie.root)

    # print('\n')
    # print(f'root_hash {trie.root_hash}')
    # trie.store('fish', 'cod')
    # print('\n')
    # pprint(trie.root)

    # print('\n')
    # print(f"first value: {trie.retrieve('animal')}")
    # print('\n')
    # print(f"second value: {trie.retrieve('fish')}")
    # print('\n')
    # print(f"thrid value: {trie.retrieve('wrong_key')}")


    trie = Trie()
    
    data ={'balance':1000}
    trx = {'data':data}
    
    trie.store(key='apple', value = trx)
    
    retrieved_trx = trie.retrieve(key='apple')
    
    print(f'retrieved_trx = {retrieved_trx}')
    
    
    data ['balance']=5000
    retrieved_trx = trie.retrieve(key='apple')
    print(f'retrieved_trx = {retrieved_trx}')
    
    