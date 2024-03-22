from django.forms import ModelForm, forms
from .models import Property, Address, Rental
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