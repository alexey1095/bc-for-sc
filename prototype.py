import requests
from pprint import pprint

url = 'http://127.0.0.1:8000'


def send_transaction(t):

    res = requests.post(url+"/api/v1/transaction", json=t, timeout=1)

    print("\n")
    pprint(res)
    pprint(res.json())
    
    
    
def request_mine():
    
    res = requests.get(url+"/api/v1/mine", timeout=1)
    
    print("\n")
    pprint(res)
    pprint(res.json())
    


if __name__ == "__main__":


#  1-----------------------------------------------
    # t = {       
    #     "to": "some address to",
    #     "amount": 100
    # }

    # send_transaction(t)

    # t = {
    #     "to": "",
    #     "amount": 0 # here can be any valid integer number (for ninja schema to work)
    # }

    # send_transaction(t)


# 2 -----------------------------------------------

    request_mine()