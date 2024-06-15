from blockchain.blockchain_util import *
from blockchain.block import genesis_block

from pubsub.pubsub import RedisPubSub
from uuid import uuid4
import json




'''The goal is to setup  a decentralized computer;, this computer will be able to track state where the blockchain 
is the core element as it stores transactions. Transactions 
describe of how the state of the decentralized computer should change. 
The blocks are shared among all participants. Participants wil take and execute new 
transactions to keep they own state up-to-date - and the state of all the 
nodes remain synchonised. ''
Anyone in the blockchain can submit a block by menas of a process called mining'''


class Blockchain:
    ''' This class defines the blockchain as a data 
    structure that primarily serves as a public 
    ledger which is shared across nodes in the network 
    and consists of a series of blocks. Each node synchrinizes it own blockchain. 
    Each block acts as a storage unit and store a series of transactions.
    '''

    def __init__(self):
        
        #  init blockchain with genesis block
        self.blockchain = [genesis_block,]
        
        self.redis = RedisPubSub(node_id=str(uuid4()))
        
        
    def append_block(self, block):
        
        if block_is_valid(self.blockchain[-1], block):
            self.blockchain.append(block)
            
             #  encoding to bytes for redis publish method
            block_encoded =  json.dumps(block) #.encode('utf-8')
            # str(block).encode('utf-8')
            # print(block_encoded)
            
            # experimentation code
            # self.redis.publish_block(b'new block publiched')
            self.redis.publish_block(block_encoded)
            return True
        
        return False
            
        

  


