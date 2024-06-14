from ninja import Router
from blockchain.blockchain import Blockchain
from blockchain.blockchain_util import mine
router = Router()
blockchain = Blockchain()


@router.get('/')
def show_hello(request):
    return[{"hello":"hi"}]


@router.get('/blockchain')
def show_blockchain(request):
    ''' show blockchain'''
    return[blockchain.blockchain]

@router.get('/mine')
def mine_block(request):
    
    # new_block = mine(blockchain.blockchain[-1], 'beneficiary')
    # blockchain.append_block(new_block)
    
    parent_block = blockchain.blockchain[-1]

    new_block = mine(parent_block['header'], 'beneficiary')

    blockchain.append_block(new_block)
    
    return[blockchain.blockchain]
