from django.urls import path, include
from rest_framework import routers

from . import views

'''router = routers.DefaultRouter()
router.register(r'properties', views.PropertyViewSet)'''

app_name = "rent_management"
urlpatterns = [
    path("", views.PropertyListView.as_view(), name='properties'),
    path("create/property", views.create_property, name='property-create'),
    path("create/address", views.create_address, name='address-create'),
]