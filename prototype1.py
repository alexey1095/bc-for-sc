import requests
from pprint import pprint
import ast
import time

url_buyer1 = 'http://127.0.0.1:8000'

url_vendor1 = 'http://127.0.0.1:8001'

url_buyer2 = 'http://127.0.0.1:8002'

url_vendor2 = 'http://127.0.0.1:8003'


def get_shipment_status_from_state(shipment_id, url_txt):

    time.sleep(1)

    txn_state = {
        "key": shipment_id
    }

    res = requests.post(url_txt+"/api/v1/state", json=txn_state, timeout=1)

    r = ast.literal_eval(res.text)

    # if r['status'] != "SHIPMENT_CREATED":
    #     print(f"error: wrong shipment status {r['status'] } ")
    #     exit()

    print(f'Shipment status: {r['status']}')


def get_previous_shipment_from_state(shipment_id, url_txt):

    time.sleep(1)

    txn_state = {
        "key": shipment_id
    }

    res = requests.post(url_txt+"/api/v1/state", json=txn_state, timeout=1)

    r = ast.literal_eval(res.text)

    return r['previous_shipment']


def init_participant(url_txt):
    res = requests.get(url_txt+"/api/v1/start", timeout=1)

    res = requests.get(url_txt+"/api/v1/account", timeout=1)

    res_dict = ast.literal_eval(res.text)

    address = res_dict['address']

    return address


def create_shipment(txn, url_buyer):

    res = requests.post(url_buyer+"/api/v1/create_shipment",
                        json=txn, timeout=1)

    res_lst = ast.literal_eval(res.text)

    shipment_id = res_lst[0]['body']['id']

    print(f'\nShipment id: {shipment_id}')

    res = requests.get(url_buyer+"/api/v1/mine", timeout=1)

    return shipment_id


if __name__ == "__main__":

    #  Init buyer1

    address_buyer1 = init_participant(url_buyer1)
    print(f'\naddress buyer1 = {address_buyer1}')

    #  Init vendor1

    address_vendor1 = init_participant(url_vendor1)
    print(f'\naddress vendor1 = {address_vendor1}')

    #  ----------- create shipment (buyer) -------------------------------

    txn = {
        "vendor": address_vendor1,
        "buyer": address_buyer1,
        "product_description": "product_description_1",
        "qty": "999",
        "price": "500",
        "contract_number": "contract num 1",
        "previous_shipment": ""
    }

    shipment_id = create_shipment(txn, url_buyer1)

    previous_shipment = get_previous_shipment_from_state(
        shipment_id, url_buyer1)
    print(f'Previous shipment id: {previous_shipment}')

    get_shipment_status_from_state(shipment_id, url_buyer1)

    #  ------------------confirm shipment -------------------------------

    txn = {

        "shipment_id": shipment_id

    }

    res = requests.post(url_vendor1+"/api/v1/confirm_shipment",
                        json=txn, timeout=1)

    res = requests.get(url_vendor1+"/api/v1/mine", timeout=1)

    get_shipment_status_from_state(shipment_id, url_vendor1)

    #  ---------------- confirm delivery ----------------------------------

    res = requests.post(url_buyer1+"/api/v1/confirm_delivery",
                        json=txn, timeout=1)

    res = requests.get(url_buyer1+"/api/v1/mine", timeout=1)

    get_shipment_status_from_state(shipment_id, url_buyer1)

    #  ___________________________________________________________________
    #  ---------------SHIPMENT 2 -------------------------------

    #  ----------- create shipment (buyer) -------------------------------

    address_buyer2 = init_participant(url_buyer2)
    print(f'\naddress buyer2 = {address_buyer2}')

    #  Init vendor1

    address_vendor2 = init_participant(url_vendor2)
    print(f'\naddress vendor2 = {address_vendor2}')

    txn = {
        "vendor": address_vendor2,
        "buyer": address_buyer2,
        "product_description": "product_description_2",
        "qty": "578",
        "price": "700",
        "contract_number": "contract num 2",
        "previous_shipment": shipment_id
    }

    shipment_id = create_shipment(txn, url_buyer2)

    previous_shipment = get_previous_shipment_from_state(
        shipment_id, url_buyer2)
    print(f'Previous shipment id: {previous_shipment}')

    get_shipment_status_from_state(shipment_id, url_buyer2)

    #  ------------------confirm shipment -------------------------------

    txn = {

        "shipment_id": shipment_id

    }

    res = requests.post(url_vendor2+"/api/v1/confirm_shipment",
                        json=txn, timeout=1)

    res = requests.get(url_vendor2+"/api/v1/mine", timeout=1)

    get_shipment_status_from_state(shipment_id, url_vendor2)

    #  ---------------- confirm delivery ----------------------------------

    res = requests.post(url_buyer2+"/api/v1/confirm_delivery",
                        json=txn, timeout=1)

    res = requests.get(url_buyer2+"/api/v1/mine", timeout=1)

    get_shipment_status_from_state(shipment_id, url_buyer2)
    
    
    # ---------------- determing provenance -------------------------------
    
    print("\n\n **************** Provenance **********************")
    
    res = requests.post(url_buyer2+"/api/v1/provenance",
                        json=txn, timeout=1)
    
    r = ast.literal_eval(res.text)
    
    
    for shipment in r:
        print ("\n")
        pprint(shipment)
        
    print("\n")
