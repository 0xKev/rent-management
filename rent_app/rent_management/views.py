from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_list_or_404, redirect
from django.urls import reverse
from django.views import generic
from .forms import PropertyCreateForm, AddressCreateForm, RentalCreateForm

from .models import Property, Address

# Create your views here.
class PropertyListView(generic.ListView):
    template_name = "rent_management/property_list.html"
    context_object_name = "properties"

    def get_queryset(self):
        properties = Property.objects.all()
        return properties
    
class AddressListView(generic.ListView):
    template_name = "rent_management/address_list.html"
    context_object_name = "addresses"
    
    def get_queryset(self):
        addresses = Address.objects.all()
        return addresses
    
def create_rental(request):
    if request.method == "POST":
        form = RentalCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("rent_management:properties")
    else:
        form = RentalCreateForm()
    
    return render(request, "rent_management/rental_create.html", {"form": form})
 
def create_property(request):
    if request.method == 'POST':
        form = PropertyCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rent_management:properties')
    else:
        form = PropertyCreateForm()
    
    return render(request, 'rent_management/property_create.html', {'form': form})

def create_address(request):
    if request.method == 'POST':
        form = AddressCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("rent_management:properties")
    else:
        form = AddressCreateForm()
    
    return render(request, 'rent_management/address_create.html', {'form': form})
    


