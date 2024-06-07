from rest_framework import serializers
from django.db import transaction
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ["id", "username"]


# using fields = "__all__" instead of list of fields bc I want all fields
class PropertySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="rent_management:property-api-detail")
    owner = serializers.ReadOnlyField(source="owner.username")
    address = serializers.HyperlinkedRelatedField(view_name="rent_management:address-api-detail", queryset=Address.objects.all(), allow_null=True)
    class Meta:
        model = Property
        exclude = ["is_active"]
 


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="rent_management:address-api-detail")
    owner = serializers.HyperlinkedIdentityField(view_name="rent_management:users-detail")
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


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class TotalTransactionsSerializer(serializers.Serializer):
    total_payment = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=10, decimal_places=2)