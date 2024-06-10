# from blockchain.block import genesis_block
from blockchain.blockchain import Blockchain
from blockchain.blockchain_util import *
from blockchain.block import genesis_block
import pprint
 

if __name__ == "__main__":

    # blockchain = Blockchain()
    
    # print(blockchain.blockchain)
    
    new_block = mine(genesis_block['header'], 'beneficiary')
    
    print('New block')
    pprint.pprint(new_block)
    