from uuid import uuid4
from typing import Type
import json
import requests
from blockchain.lib import *
from blockchain.block import genesis_block

from pubsub.pubsub import RedisPubSub
from state.state import State


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

    def __init__(self, account, state:Type[State]):

        #  init blockchain with genesis block
        self.blockchain = [genesis_block,]

        #  unique randomly generated node's id
        self.node_id = uuid4().hex
        
        self.account = account

        self.redis = RedisPubSub(node_id=self.node_id, blockchain=self, account=self.account)
        
        self.state = state
        
        self.block_reward = 100
    

    def _synchronize(self, peer_url):
        ''' getting the latest version of the blockchain '''

        try:
            response = requests.get(peer_url, timeout=1)
            response.raise_for_status()

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
    
    
    def synchronize_blockchain(self, url):
        try:
            response = self._synchronize(
                peer_url=url)

            status = self.update_blockchain(response)           

            if status:
                return self.blockchain
            else:
                return "ERROR: FAILS TO UPDATE THE BLOCKCHAIN"

        except ValueError as e:
            return e

    def append_block(self, block, notify=True):
        ''' appends a valid new block to the blockchain '''
                
        if not block_is_valid(self.blockchain[-1], block):
            print('\n ERROR: VALIDATION FAILED - BLOCK HAS BEEN REJECTED BY BLOCKCHAIN')
            return False

        self.blockchain.append(block)
        
        
        # update state by processing the block        
        self.state.process_block(block)
        
        
        
        # state.
        
        #  once the block is added we want to remove those transactions from 
        #  the transaction pool
        
        self.account.remove_transactions_added_to_block(block['transactions'])
        
        

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
        # of the synchronization process `rename to synchronize_blockchain`
        
        #  check if we need to update the blockchain
        hash_existing_blockchain = generate_keccak256_hash(
            self.blockchain
            )
        hash_sent_blockchain = generate_keccak256_hash(blockchain)
        
        if hash_existing_blockchain == hash_sent_blockchain:
            print("\n -- No need to synchronize the blockchain ")
            return True
                
        #  no need to update the upcoming blockchain consists of only one genesis block
        if len(blockchain) == 1:
            return True
        
        for index, block in enumerate(blockchain):
            
            if index == 0:
                continue
            
            
            if not block_is_valid(blockchain[index-1], block):
                print('\n ERROR: VALIDATION FAILED - BLOCK HAS BEEN REJECTED BY BLOCKCHAIN')
                print('++++++ LOCAL BLOCKCHAIN HAS NOT BEEN UPDATED +++++++')
                return False
            
            #  update the state by processing a block
            self.state.process_block(block)
        
        self.blockchain = blockchain
        
        
        print('\n++++++ LOCAL BLOCKCHAIN HAS BEEN UPDATED +++++++\n')
        return True
    
    
    def create_shipment(self, vendor, buyer, product_description, qty, price, contract_number,previous_shipment):
           #  create new shipment transaction (wrapper)
        txn_shipment = self.account.generate_new_shipment_transaction(
            vendor=vendor,
            buyer=buyer,
            product_description=product_description,
            qty=qty,
            price=price,
            contract_number=contract_number,
            previous_shipment=previous_shipment
        )

        if not self.account.add_transaction_to_pool(txn_shipment):
            return {
                'Error': 'Transaction is not valid',
                'Details': txn_shipment}
            
        self.redis.publish_transaction(str(txn_shipment))

        # generate currency blocking txn
        txn_blocking = self.account.generate_currency_blocking_transaction(
            amount=price,
            ref_txn_id=txn_shipment['body']['id'])

        #  adding blocking transaction to transaction pool and publish

        if not self.account.add_transaction_to_pool(txn_blocking):
            return {
                'Error': 'Transaction is not valid',
                'Details': txn_blocking}

        self.redis.publish_transaction(str(txn_blocking))

        return ([txn_shipment, txn_blocking])
            
        
    def confirm_shipment(self, shipment_id):
        
        txn_shipment = self.account.generate_confirm_shipment_or_delivery_transaction(
            shipment_id=shipment_id, transaction_type=TransactionType.CONFIRM_SHIPMENT_TRANSACTION
            )

        if not self.account.add_transaction_to_pool(txn_shipment):
            return {
                'Error': 'Transaction is not valid',
                'Details': txn_shipment}
        self.redis.publish_transaction(str(txn_shipment))

        return (txn_shipment)
    
    
    def confirm_delivery(self, shipment_id):
        
            #  create new shipment transaction
        txn_shipment = self.account.generate_confirm_shipment_or_delivery_transaction(
            shipment_id=shipment_id, transaction_type=TransactionType.CONFIRM_DELIVERY_TRANSACTION
        )

        if not self.account.add_transaction_to_pool(txn_shipment):
            return {
                'Error': 'Transaction is not valid',
                'Details': txn_shipment}
        self.redis.publish_transaction(str(txn_shipment))

        return ([txn_shipment])
        
        
