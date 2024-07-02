# node/urls.py
from django.urls import path

from . import views
# from sc_client import views as sc_client_view

urlpatterns = [
    # path("", views.index, name="node"),
    # path("sc_client/", sc_client_view.index, name="index_sc_client"),
    # path("", views.index, name="roomdd"),
    path("<str:room_name>/", views.room, name="room"),
    
]