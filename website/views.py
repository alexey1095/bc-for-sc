from django.http import HttpResponse
from django.shortcuts import render
from api.v1 import blockchain

def index(request):
    # return HttpResponse('<H1>GO TO /api/v1/start </H1>')
    
    port = None
    
    gelenIleti = request.META.get('HTTP_X_FORWARDED_FOR')

    if gelenIleti:

        ip = gelenIleti.split(',')[0]

    else:

        ip = request.META.get('REMOTE_ADDR')

        port = request.META['SERVER_PORT']
    
    
    
    node_id = blockchain.node_id
    context = {'node_id':node_id, 'ip':ip, 'port':port}
    return render(request, "index.html", context )