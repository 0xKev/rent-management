from django.forms import ModelForm, ModelChoiceField
from .models import Property, Address, Rental, Tenant
from django.core.exceptions import ValidationError

class PropertyCreateForm(ModelForm):
    class Meta:
        model = Property
        fields = '__all__'

class AddressCreateForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

class RentalCreateForm(ModelForm):
    class Meta:
        model = Rental
        fields = '__all__'

    #asset = ModelChoiceField(queryset=Property.objects.all()) # ModelChoiceField presents choices from model queryset as dropdown select elements
    #tenant = ModelChoiceField(queryset=Tenant.objects.all())