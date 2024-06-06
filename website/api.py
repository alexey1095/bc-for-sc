from ninja import NinjaAPI

from api.v1 import router as router_v1

api = NinjaAPI()

api.add_router("v1", router_v1)

