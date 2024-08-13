from django.urls import path

from . import views


urlpatterns = [    
    path("confirm_delivery/", views.confirm_delivery, name='confirm_delivery'),
    path("confirm_shipment/", views.confirm_shipment, name='confirm_shipment'),
    path("create_shipment/", views.create_shipment, name='create_shipment'),
    path("<str:node_id>/", views.node, name="node_page"),
      
]