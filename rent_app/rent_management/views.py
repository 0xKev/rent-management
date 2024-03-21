from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_list_or_404, redirect
from django.urls import reverse
from django.views import generic
from .forms import PropertyCreateForm, AddressCreateForm

from .models import Property

# Create your views here.
class PropertyListView(generic.ListView):
    template_name = "rent_management/property_list.html"
    context_object_name = "properties"

    def get_queryset(self):
        properties = Property.objects.all()
        return properties
    
def create_property(request):
    if request.method == 'POST':
        form = PropertyCreateForm(request.POST)
        address_pk = reverse('address-create', args=[str.id)])
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
    


