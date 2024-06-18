from ninja import Router
from ninja import Schema
from blockchain.blockchain import Blockchain
from account.account import Account
from account.account import TransactionType
from blockchain.blockchain_util import mine
import json
router = Router()

blockchain = Blockchain()
# blockchain.get_blockchain()

#  create an account
account = Account()
account.generate_transaction(account)


# https://medium.com/@marcnealer/django-ninja-the-contender-217b80b0e1e7
class Transaction(Schema):
    type: str
    to: str
    amount: int


@router.post('/transaction', description="Creates a transaction")
def create_new_transaction(request, transaction: Transaction):

    try:
        t_type = TransactionType[transaction.type]
    except Exception as e:
        return {"Error": "wrong transaction type",
                "Message": str(e)}

    tt = account.generate_transaction(
        transact_type=t_type,
        to=transaction.to,
        amount=transaction.amount
    )
    
    # ss = json.dumps(tt)

    return str(tt)


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

    new_block = mine(
        parent_header=parent_block['header'],
        beneficiary=account.address
    )

    blockchain.append_block(new_block)

    return blockchain.blockchain


@router.get('/synchronize')
def synchronize_blockchain(request):
    ''' synchronizing the local blockchain with the latest version of the blockchain'''

    try:
        response = blockchain.synchronize(
            peer_url='http://127.0.0.1:8000/api/v1/blockchain')

        status = blockchain.update_blockchain(response)

        if status:
            return blockchain.blockchain
        else:
            return "ERROR: FAILS TO UPDATE THE BLOCKCHAIN"

    except ValueError as e:
        return e
