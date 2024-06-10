from rest_framework import serializers
from django.db import transaction
from .models import *
from accounts.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser 
        fields = ["id", "username"]


# using fields = "__all__" instead of list of fields bc I want all fields
class PropertySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="rent_management:property-api-detail")
    owner = serializers.ReadOnlyField(source="owner.username")
    address = serializers.HyperlinkedRelatedField(view_name="rent_management:address-api-detail", queryset=Address.objects.all(), allow_null=True)
    rental_set = serializers.HyperlinkedIdentityField(view_name="rent_management:rental-api-detail", read_only=True, allow_null=True, many=True)

    class Meta:
        model = Property
        exclude = ["is_active"]
 


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="rent_management:address-api-detail")
    owner = serializers.HyperlinkedIdentityField(view_name="rent_management:users-detail")
    class Meta:
        model = Address
        fields = "__all__"


class RentalSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="rent_management:rental-api-detail")
    owner = serializers.ReadOnlyField(source="owner.username")
    property = serializers.HyperlinkedRelatedField(view_name="rent_management:property-api-detail", queryset=Property.objects.all())
    tenant = serializers.HyperlinkedRelatedField(view_name="rent_management:tenant-api-detail", queryset=Tenant.objects.all())
    class Meta:
        model = Rental
        fields = "__all__"

    def validate(self, attrs):
        property = attrs.get("property")
        if property.status != "available":
            raise serializers.ValidationError("Property not available for rental.")
        return super().validate(attrs)


class TenantSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    url = serializers.HyperlinkedIdentityField(view_name="rent_management:tenant-api-detail")
    address = serializers.HyperlinkedIdentityField(view_name="rent_management:address-api-detail")
    class Meta:
        model = Tenant
        fields = "__all__"


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="rent_management:payment-api-detail")
    owner = serializers.ReadOnlyField(source="owner.username")
    rental = serializers.HyperlinkedRelatedField(view_name="rent_management:rental-api-detail", queryset=Rental.objects.all())
    class Meta:
        model = Payment
        fields = ["url", "owner", "created", "updated", "rental", "payment_amount", "date_paid", "description"]


class ExpenseSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="rent_management:expense-api-detail")
    owner = serializers.ReadOnlyField(source="owner.username")
    rental = serializers.HyperlinkedRelatedField(view_name="rent_management:rental-api-detail", queryset=Rental.objects.all(), allow_null=True)
    property = serializers.HyperlinkedRelatedField(view_name="rent_management:property-api-detail", queryset=Property.objects.all())
    class Meta:
        model = Expense
        fields = ["url", "owner", "created", "updated", "rental", "property", "payment_amount", "date_paid", "description"]


class TotalTransactionSerializer(serializers.Serializer):
    properties = serializers.HyperlinkedRelatedField(many=True, view_name="rent_management:property-api-detail", queryset=Property.objects.all())
    rentals = serializers.HyperlinkedRelatedField(many=True, view_name="rent_management:rental-api-detail", queryset=Rental.objects.all())
    total_payments = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=10, decimal_places=2)

