from uuid import uuid4
import json
import requests
from blockchain.blockchain_util import *
from blockchain.block import genesis_block

from pubsub.pubsub import RedisPubSub


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

    def __init__(self, account):

        #  init blockchain with genesis block
        self.blockchain = [genesis_block,]

        #  this is a peer url that can provide the latest version of the blockchain
        # self.peer_url = peer_url

        #  unique randomly generated node's id
        self.node_id = str(uuid4())
        
        self.account = account

        self.redis = RedisPubSub(node_id=self.node_id, blockchain=self, account=self.account)
        
       

    # def redis_block_channel_handler(self, payload):
    #     ''' this is a callback function from the `RedisPubSub` class fro the `BLOCK` channel'''

    #     print("this is redis handler from Blockchain class")
    #     pprint(payload)

    def synchronize(self, peer_url):
        ''' getting the latest version of the blockchain '''

        try:
            response = requests.get(peer_url)
            response.raise_for_status()

            # print('HTTP reponse :')
            # pprint(response.json())

        except requests.ConnectionError as e:
            print(e)
            raise ValueError (f'Blockchain Synchronization Error {e}') from e

        except requests.exceptions.HTTPError as e:
            print(e)
            raise ValueError (f'Blockchain Synchronization Error {e}') from e  
        
        except requests.exceptions.RequestException as e:
            print(e)
            raise ValueError (f'Blockchain Synchronization Error {e}') from e 
                   
        return response.json()

    def append_block(self, block, notify=True):
        ''' appends a valid new block to the blockchain '''

        if not block_is_valid(self.blockchain[-1], block):
            print('\n ERROR: VALIDATION FAILED - BLOCK HAS BEEN REJECTED BY BLOCKCHAIN')
            return False

        self.blockchain.append(block)

        #  encoding to bytes for redis publish method
        block_encoded = json.dumps(block)

        # publish a new block on the `BLOCK` channel only if the block 
        #  is created by the given node - we dont want to publish when
        #  block was broadcasted
        if notify:
            self.redis.publish_block(block_encoded)

        print("\n >>>>>>>>>>> BLOCK HAS BEEN ADDED TO BLOCKCHAIN <<<<<<<<<<<")

        return True
    
    def update_blockchain(self, blockchain):
        # update  local version of the blockchain with the 
        # latest version, this is typicall done as a part 
        # of the synchronization process
                
        #  no need to update the upcoming blockchain consists of only one genesis block
        if len(blockchain) == 1:
            return True
        
        for index, block in enumerate(blockchain):
            
            # if index == 0:
            #     continue
            
            
            if not block_is_valid(blockchain[index-1], block):
                print('\n ERROR: VALIDATION FAILED - BLOCK HAS BEEN REJECTED BY BLOCKCHAIN')
                print('++++++ LOCAL BLOCKCHAIN HAS NOT BEEN UPDATED +++++++')
                return False
        
        self.blockchain = blockchain
        print('\n++++++ LOCAL BLOCKCHAIN HAS BEEN UPDATED +++++++\n')
        return True
            
        
        
        
