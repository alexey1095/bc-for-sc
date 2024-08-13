# from django.test import TestCase
# from state.state import State
# from blockchain.blockchain import Blockchain
# from account.account import Account
# from blockchain.lib import mine_block
# # Create your tests here.

# import time


# class ShipmentTests(TestCase):

#     def setUp(self):
#         self.state = State()
#         self.vendor = Account(self.state)

#         self.blockchain_vendor = Blockchain(self.vendor, self.state)

#         self.buyer = Account(self.state)

#         self.blockchain_buyer = Blockchain(self.buyer, self.state)

#         vendor_account_transaction = self.vendor.generate_account_transaction()
#         buyer_account_transaction = self.buyer.generate_account_transaction()

#         self.vendor.add_transaction_to_pool(vendor_account_transaction)
#         self.vendor.add_transaction_to_pool(buyer_account_transaction)

#         b = mine_block(self.blockchain_vendor, self.vendor, self.state)
        
#         time.sleep(5) 

#     def test_create_shipment(self):

#         res = self.blockchain_buyer.create_shipment(
#             vendor=self.vendor.address,
#             buyer=self.buyer.address,
#             product_description="product_description_1",
#             qty="100",
#             price=500,
#             contract_number="Contract 1",
#             previous_shipment="origin")
        
#         b = mine_block(self.blockchain_buyer, self.buyer, self.state)
        
        


#         shipment_id = res[0]['body']['id']

#         print(f'#### shipment_id= {shipment_id}')

#         self.assertIsNotNone(shipment_id)
        
        
#     def test_confirm_shipment(self):

       
#         res = self.blockchain_buyer.create_shipment(
#             vendor=self.vendor.address,
#             buyer=self.buyer.address,
#             product_description="product_description_1",
#             qty="100",
#             price=500,
#             contract_number="Contract 1",
#             previous_shipment="origin")
        
#         time.sleep(3)
        
#         b = mine_block(self.blockchain_buyer, self.buyer, self.state)
        
#         shipment_id = res[0]['body']['id']

#         print(f'#### shipment_id= {shipment_id}')
        
#         time.sleep(3)
        
#         res1= self.blockchain_vendor.confirm_shipment(shipment_id)
        
#         time.sleep(3)
        
#         b = mine_block(self.blockchain_vendor, self.vendor, self.state)
        
#         time.sleep(3)
        
#         shipment_status = self.state.retrieve_state_value(shipment_id)['status']
        
#         print('**** Shipemnt Status')
        
#         print(shipment_status)
        
        
        
#         self.assertEqual(shipment_status, "SHIPMENT_CONFIRMED")
        

#         # self.assertIsNotNone(shipment_id)
        
        
#     def test_confirm_delivery(self):

       
#         res = self.blockchain_buyer.create_shipment(
#             vendor=self.vendor.address,
#             buyer=self.buyer.address,
#             product_description="product_description_1",
#             qty="100",
#             price=500,
#             contract_number="Contract 1",
#             previous_shipment="origin")
        
#         time.sleep(3)
        
#         b = mine_block(self.blockchain_buyer, self.buyer, self.state)
        
#         shipment_id = res[0]['body']['id']

#         print(f'#### shipment_id= {shipment_id}')
        
#         time.sleep(3)
        
#         res1= self.blockchain_vendor.confirm_shipment(shipment_id)
        
#         time.sleep(3)
        
#         b = mine_block(self.blockchain_vendor, self.vendor, self.state)
        
#         time.sleep(3)
        
#         # -----------------------
        
#         res1= self.blockchain_buyer.confirm_delivery(shipment_id)
        
#         time.sleep(3)
        
#         b = mine_block(self.blockchain_buyer, self.buyer, self.state)
        
#         time.sleep(3)
        
#         shipment_status = self.state.retrieve_state_value(shipment_id)['status']
        
#         print('**** Shipemnt Status')
        
#         print(shipment_status)
        
        
        
#         self.assertEqual(shipment_status, "SHIPMENT_DELIVERED")
        
        
    

       