import requests
from ninja import Router
from ninja import Schema
from blockchain.blockchain import Blockchain
from account.account import Account
from account.account import TransactionType
from state.state import State
from blockchain.lib import mine_block
from shipment.shipment_status import *
import json
import time
from pprint import pprint
# from node.ws_consumer

import asyncio
from websockets.sync.client import connect
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

router = Router()

state = State()

account = Account(state)

blockchain = Blockchain(account, state)


@router.get('/start', description="Initialize a user")
def start(request):
    ''' We need to call this end point to properly setup the accounts'''

    print(f'\nAccount address: {account.address}\n')    

    new_account_transaction = account.generate_account_transaction()

    if not account.add_transaction_to_pool(new_account_transaction):
        return {
            'Error': 'Transaction is not valid',
            'Details': new_account_transaction}    

    #  we need to synchronize the blockchain before mining any blocks to avoid errors
    blockchain.synchronize_blockchain(
        'http://127.0.0.1:8000/api/v1/blockchain')

    # we need to publish a message before mining a block for the peer to correctly remove transaction from pool
    new_account_transaction_encoded = json.dumps(new_account_transaction)
    blockchain.redis.publish_transaction(msg=new_account_transaction_encoded)

    # we need to call mine block here to add a new account to the state
    res = mine_block(blockchain, account, state)

    return blockchain.blockchain


# https://medium.com/@marcnealer/django-ninja-the-contender-217b80b0e1e7
class Transaction(Schema):
    to: str
    amount: int


@router.post('/transaction', description="Creates a transaction")
def create_new_transaction(request, transaction: Transaction):   

    tt = account.generate_currency_transaction(

        to=transaction.to,
        amount=transaction.amount
    )

    pprint(tt)

    if not account.add_transaction_to_pool(tt):
        return {
            'Error': 'Transaction is not valid',
            'Details': tt}

    # tt_encoded = json.dumps(tt)
    tt_encoded = str(tt)

    blockchain.redis.publish_transaction(tt_encoded)

    # ss = json.dumps(tt)

    return (tt)


class CreateShipment(Schema):
    vendor: str
    buyer: str # added
    product_description: str
    qty: int
    price: int
    contract_number: str
    previous_shipment: str
    # action: str  # create_shipment, confirm_shipment, confirm_delivery


@router.post('/create_shipment', description="Creates a shipment")
def create_shipment_api_end_point(request, shipment: CreateShipment):
    
    
    res = blockchain.create_shipment(
        vendor=shipment.vendor,
        # buyer=account.address,
        buyer=shipment.buyer,
        product_description=shipment.product_description,
        qty=shipment.qty,
        price=shipment.price,
        contract_number=shipment.contract_number,
        previous_shipment=shipment.previous_shipment
    )
    
    return (res)
   

class ShipmentId(Schema):
    shipment_id: str


@router.post('/confirm_shipment', description="Confirm shipment transaction")
def confirm_shipment_api_end_point(request, shipment: ShipmentId):
    
    
    res= blockchain.confirm_shipment(shipment.shipment_id)
    
    return res

@router.post('/confirm_delivery', description="Confirm delivery ")
def confirm_delivery_api_end_point(request, shipment: ShipmentId):
    
    res= blockchain.confirm_delivery(shipment.shipment_id)
    
    return res  


@router.get('/state')
def show_state(request):
    return state.state_trie.root

#  -------------------------------------------------------------------


class StateKey(Schema):
    key: str


@router.post('/state', description=" retrieve state for a sent key")
def show_state_value_api_end_point(request, received_key: StateKey):

    value = state.retrieve_state_value(key=received_key.key)

    if not value:
        return {'ERROR': f'The key {received_key.key} does not exist in state'}

    return value

#  ------------------------------------------------------------------


@router.post('/provenance', description=" get provenance for a sent shipemnt id")
def show_provenance_api_end_point(request, shipment: ShipmentId):   

    shipments = []

    shipment_id = shipment.shipment_id

    while True:

        shipment = state.retrieve_state_value(key=shipment_id)

        if not shipment:
            return {'ERROR': f'The key {shipment_id} does not exist in state'}

        shipments.append(shipment)

        shipment_id = shipment['previous_shipment']

        if shipment_id == 'origin':
            break

    return shipments


@router.get('/transaction', description="Show transaction pool")
def show_transaction(request):

    return account.transaction_pool


@router.get('/')
def show_hello(request):
    return "Hello"


@router.get('/blockchain')
def show_blockchain(request):
    ''' show blockchain'''
    return blockchain.blockchain


@router.get('/mine')
def mine_block_request(request):

    return mine_block(blockchain, account, state)
   

@router.get('/synchronize')
def synchronize_blockchain_request(request):
    ''' synchronizing the local blockchain with the latest version of the blockchain'''

    blockchain.synchronize_blockchain(
        'http://127.0.0.1:8000/api/v1/blockchain')


@router.get('/account')
def show_account(request):
    return {
        'address': account.address,
        'balance': state._retrieve_account_balance(account.address)
    }

@router.get('/send_message')
def send_message(request):
    ''' Send message to node '''
    

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'node_{blockchain.node_id}',
        {
            'type': 'node_message',
            'message': "Hi from the backend"
        }
    )

    return {
        'status': 'message hopefully sent'

    }
