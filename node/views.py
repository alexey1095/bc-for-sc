from django.shortcuts import render
from django.http import HttpResponse
from api.v1 import blockchain
from . forms import *

# Create your views here.

# def index(request):
#     return render(request, "node.html")


def node(request, node_id):
    return render(request, "node.html", {
        "node_id": node_id,
        "create_shipment_form": CreateShipmentForm()
        })


def create_shipment(request):
    
    if request.method =='POST':
        form = CreateShipmentForm(request.POST)
        
        if form.is_valid():
            return HttpResponse("<h3>Form is Valid</h3>")
    
    return HttpResponse('<h3>Only POST is allowed</h3>')    
        
    
    
    
    # return render(request, "node.html", {"node_id": node_id})


# def index(request):
#     # return HttpResponse('<H1>GO TO /api/v1/start </H1>')

#     port = None

#     gelenIleti = request.META.get('HTTP_X_FORWARDED_FOR')

#     if gelenIleti:

#         ip = gelenIleti.split(',')[0]

#     else:

#         ip = request.META.get('REMOTE_ADDR')

#         port = request.META['SERVER_PORT']


#     node_id = blockchain.node_id
#     context = [node_id, ip, port]
#     return render(request, "index.html", context )
