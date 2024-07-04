from django import forms


class CreateShipmentForm(forms.Form):
    vendor = forms.CharField(label="Vendor address", max_length=500)
    product_description = forms.CharField(label="Description of the product", max_length=500, initial="product_1")
    qty = forms.IntegerField(label='Q-ty', initial='100')
    price = forms.IntegerField(label='Price', initial="500")
    contract_number = forms.CharField(label="Contract number", max_length=100, initial="contract_1")
    previous_shipment = forms.CharField(label="Previous shipment", max_length=100, initial="")
    

class ConfirmShipmentForm(forms.Form):
    shipment_id = forms.CharField(label="Shipment ID:", max_length=500)
    
    
class ConfirmDeliveryForm(forms.Form):
    shipment_id = forms.CharField(label="Shipment ID:", max_length=500)
    