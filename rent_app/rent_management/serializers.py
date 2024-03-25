from rest_framework import serializers
from django.db import transaction
from .models import Property, Address, Rental, Tenant


# using fields = "__all__" instead of list of fields bc I want all fields
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = "__all__"

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = "__all__"
    
