from django.shortcuts import render
from django.http import HttpResponse
from api.v1 import blockchain

# Create your views here.

# def index(request):
#     return render(request, "node.html")


def room(request, room_name):
    return render(request, "node.html", {"room_name": room_name})




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