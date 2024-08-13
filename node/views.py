from django.shortcuts import render
from django.http import HttpResponse
from api.v1 import blockchain
from . forms import *
from api.v1 import account


def node(request, node_id):
    return render(request, "node.html", {
        "node_id": node_id,
        "self_address": account.address,
        "create_shipment_form": CreateShipmentForm(),
        "confirm_shipment_form": ConfirmShipmentForm(),
        "confirm_delivery_form": ConfirmDeliveryForm(),
    })


def create_shipment(request):

    if request.method != 'POST':
        return HttpResponse('<h3>Only POST is allowed</h3>')

    form = CreateShipmentForm(request.POST)

    if not form.is_valid():
        return HttpResponse("<h3>Form is not valid</h3>")

    vendor = form.cleaned_data['vendor']
    product_description = form.cleaned_data['product_description']
    qty = form.cleaned_data['qty']
    price = form.cleaned_data['price']
    contract_number = form.cleaned_data['contract_number']
    previous_shipment = form.cleaned_data['previous_shipment']

    res = blockchain.create_shipment(
        vendor=vendor,
        buyer=account.address,
        product_description=product_description,
        qty=qty,
        price=price,
        contract_number=contract_number,
        previous_shipment=previous_shipment
    )

    return HttpResponse('<p>' + str(res)+'</p>')


def confirm_shipment(request):

    if request.method != 'POST':
        return HttpResponse('<h3>Only POST is allowed</h3>')

    form = ConfirmShipmentForm(request.POST)

    if not form.is_valid():
        return HttpResponse("<h3>Form is not valid</h3>")

    shipment_id = form.cleaned_data['shipment_id']

    res = blockchain.confirm_shipment(shipment_id)

    return HttpResponse('<p>' + str(res)+'</p>')


def confirm_delivery(request):

    if request.method != 'POST':
        return HttpResponse('<h3>Only POST is allowed</h3>')

    form = ConfirmDeliveryForm(request.POST)

    if not form.is_valid():
        return HttpResponse("<h3>Form is not valid</h3>")

    shipment_id = form.cleaned_data['shipment_id']

    res = blockchain.confirm_delivery(shipment_id)

    return HttpResponse('<p>' + str(res)+'</p>')

