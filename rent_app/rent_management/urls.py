from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'properties', views.PropertyViewSet, basename="property-api")
router.register(r'addresses', views.AddressViewSet, basename="address-api") # using just 'address' conflicts with path 'address-list bc router auto generates various urls
router.register(r'rentals', views.RentalViewSet, basename="rental-api")
router.register(r'tenants', views.TenantViewSet, basename="tenant-api")
router.register(r'finances', views.TotalTransactionsViewSet, basename="total-api")
router.register(r'payments', views.PaymentViewSet, basename="payment-api")
router.register(r'expenses', views.ExpenseViewSet, basename="expense-api")

app_name = "rent_management"
urlpatterns = [
    path("", views.PropertyListView.as_view(), name='properties'),
    path("api/", include(router.urls)),
    path("create-property", views.create_property, name='property-create'),
    path("create-address", views.create_address, name='address-create'),
    path("view-address/", views.AddressListView.as_view(), name="address-list"),
    path("create-rental", views.create_rental, name="rental-create"),
    path("view-rentals/", views.RentalListView.as_view(), name="rental-list")
]