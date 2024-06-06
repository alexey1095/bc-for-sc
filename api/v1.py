from ninja import Router

router = Router()

@router.get('/')
def show_hello(request):
    return[{"hello":"hi"}]