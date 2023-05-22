from django.urls import path
from . import views

app_name = 'inventory'
urlpatterns = [
    path(route='received/', view=views.received_detail, name='received'),
    path(route='issued/', view=views.issued_detail, name='issued'),
    path(route='detail/', view=views.inventory_detail, name='detail'),
    path(route='items/', view=views.item_list, name='items'),
    path(route='received-bill/<int:pk>', view=views.inventory_received_bill_detail, name='received-bill'),
    path(route='issued-bill/<int:pk>', view=views.inventory_issued_bill_detail, name='issued-bill')
]
