from ninja import Router
from ninja import Schema
from blockchain.blockchain import Blockchain
from account.account import Account
from account.account import TransactionType
from blockchain.blockchain_util import mine
import json
import time
from pprint import pprint
router = Router()


account = Account()

blockchain = Blockchain(account)
# blockchain.get_blockchain()
new_account_transaction = account.generate_transaction(to=None)

account.add_transaction_to_pool(new_account_transaction)

pprint(new_account_transaction)

new_account_transaction_encoded = json.dumps(new_account_transaction)


blockchain.redis.publish_transaction(msg=new_account_transaction_encoded)


# transaction should be in the local pool

time.sleep(1)
print("\ntransaction pool contene:")
pprint(account.transaction_pool)



#  create an account
# account = Account()
# account.generate_transaction(account)


# https://medium.com/@marcnealer/django-ninja-the-contender-217b80b0e1e7
class Transaction(Schema):    
    to: str
    amount: int


@router.post('/transaction', description="Creates a transaction")
def create_new_transaction(request, transaction: Transaction):

    # try:
    #     t_type = TransactionType[transaction.type]
    # except Exception as e:
    #     return {"Error": "wrong transaction type",
    #             "Message": str(e)}       
            

    tt = account.generate_transaction(
       
        to=transaction.to,
        amount=transaction.amount
        
        
    )
    
    pprint(tt)
    
    account.add_transaction_to_pool(tt)
    
    # tt_encoded = json.dumps(tt)
    tt_encoded = str(tt)
    
    blockchain.redis.publish_transaction(tt_encoded)
    
    # ss = json.dumps(tt)

    return (tt)


@router.get('/transaction', description="Show transaction pool")
def show_transaction(request):
    
    return account.transaction_pool



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
    
    transactions = account.return_transaction_pool()

    new_block = mine(
        parent_header=parent_block['header'],
        beneficiary=account.address,
        transactions=transactions
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
