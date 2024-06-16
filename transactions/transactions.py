from enum import Enum

'''Transactions will serve two overall purposes. The first one is to excgange currency between accounts.

Transactions will change the state of the decentralized computer - 

In Ethereum transactions do more than exchange currency between accounts - they describe how the state of the decentralized computer changes.

There are two types of trrqansactions - to exchange currecmcy and to registere the account.'''


class TransactionType(Enum):

    CURRENCY_TRANSACTION = 'CURRENCY_TRANSACTION'
    NEW_ACCOUNT_TRANSACTION = 'NEW_ACCOUNT_TRANSACTION'


class Transaction:

    def __init__(self):
        pass
