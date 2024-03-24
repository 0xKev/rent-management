from rest_framework import serializers
from django.db import transaction
from .models import Property, Address, Rental


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

    @transaction.non_atomic_requests
    def create(self, validated_data):
        """
        Create and return new 'Rental' instance given validated data and update 'Property' status to 'rented'
        """
        ### IMPLEMENT django transaction to prevent partial data modification in case of error ###
        
        property_obj = validated_data.get('property')

        if property_obj.status != 'rented':
            rental = Rental(**validated_data)
            rental.save()
            property_obj.status = 'rented'
            property_obj.save()
            return rental
        else:
            raise serializers.ValidationError("Property has already been rented!")
        
    '''def destroy(self, validated_data, *args, **kwargs):
        #### FIX SO RENTED BECOMES AVAILABLE WHEN RENTAL DELETED ####
        rental_instance = self.get_object()
        property_instance = rental_instance.property

        if property_instance.status == 'rented':
            property_instance.status = 'available'
            property_instance.save()
        
        return super().destroy(validated_data, *args, **kwargs)'''
    
