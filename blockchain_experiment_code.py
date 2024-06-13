# from blockchain.block import genesis_block
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from blockchain.blockchain import Blockchain
from blockchain.blockchain_util import *
from blockchain.block import genesis_block
import pprint
import sys


if __name__ == "__main__":

    # blockchain = Blockchain()

    # print(blockchain.blockchain)

    # ---------------------------------------------

    # new_block = mine(genesis_block['header'], 'beneficiary')

    # print('New block')
    # pprint.pprint(new_block)

    # -----------------------------------------------

    # parent_timestamp = datetime.now()
    # current_timestamp = parent_timestamp + relativedelta(seconds=90)

    # difficulty = adjust_difficulty(current_timestamp, parent_timestamp, 0)

    # ---------------------------------------------------

    blockchain = Blockchain()

    for i in range(100):

        parent_block = blockchain.blockchain[-1]

        new_block = mine(parent_block['header'], 'beneficiary')

        if not blockchain.append_block(new_block):
            sys.exit()
            

    print('\n')
    pprint.pprint(blockchain.blockchain)
