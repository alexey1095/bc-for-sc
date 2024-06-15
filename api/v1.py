from ninja import Router
from blockchain.blockchain import Blockchain
from blockchain.blockchain_util import mine
import json
router = Router()

blockchain = Blockchain()
# blockchain.get_blockchain()


@router.get('/')
def show_hello(request):
    return [{"hello": "hi"}]


@router.get('/blockchain')
def show_blockchain(request):
    ''' show blockchain'''
    return blockchain.blockchain


@router.get('/mine')
def mine_block(request):

    # new_block = mine(blockchain.blockchain[-1], 'beneficiary')
    # blockchain.append_block(new_block)

    parent_block = blockchain.blockchain[-1]

    new_block = mine(parent_block['header'], 'beneficiary')

    blockchain.append_block(new_block)

    return blockchain.blockchain


@router.get('/synchronize')
def synchronize_blockchain(request):
    ''' synchronizing the local blockchain with the latest version of the blockchain'''

    try:
        response = blockchain.synchronize(
            peer_url='http://127.0.0.1:8080/api/v1/blockchain')

        status = blockchain.update_blockchain(response)

        if status:
            return blockchain.blockchain

        else:
            return "ERROR: FAILS TO UPDATE THE BLOCKCHAIN"

    except ValueError as e:
        return e
