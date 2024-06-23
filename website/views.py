from django.http import HttpResponse

def index(request):
    return HttpResponse('<H1>GO TO /api/v1/start </H1>')