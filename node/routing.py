# node/routing.py
from django.urls import re_path

from . import ws_consumer
# from sc_client import sc_consumers

# websocket_urlpatterns = [
#     re_path(r"ws/node/", ws_consumer.NodeWebSocketConsumer.as_asgi()),
#     # re_path(r"ws/node/(?P<room_name>\w+)/$", consumers.NodeConsumer.as_asgi()),
    
# ]

websocket_urlpatterns = [
    re_path(r"ws/node/(?P<node_id>\w+)/$", ws_consumer.NodeConsumer.as_asgi()),
]