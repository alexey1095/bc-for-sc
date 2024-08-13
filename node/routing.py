from django.urls import re_path

from . import ws_consumer

websocket_urlpatterns = [
    re_path(r"ws/node/(?P<node_id>\w+)/$", ws_consumer.NodeConsumer.as_asgi()),
]