from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from .forms import PropertyCreateForm, AddressCreateForm, RentalCreateForm
from django.db import transaction

from .models import Property, Address, Rental, Tenant, Payment, Expense

#### for Django Rest Framework
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.schemas import get_schema_view
from rest_framework import permissions

### permissions.py for development and production ###
from .permissions import DevelopmentModelPermission, get_custom_permissions
from accounts.models import CustomUser

class PropertyListView(generic.ListView):
    template_name = "rent_management/property_list.html"
    context_object_name = "properties"

    def get_queryset(self):
        properties = Property.objects.all()
        return properties
    
    def get_permissions(self):
        return get_custom_permissions(self.request)
    
class AddressListView(generic.ListView):
    template_name = "rent_management/address_list.html"
    context_object_name = "addresses"
    
    def get_queryset(self):
        addresses = Address.objects.all()
        return addresses
    
    def get_permissions(self):
        return get_custom_permissions(self.request)
    
class RentalListView(generic.ListView):
    template_name = "rent_management/rental_list.html"
    context_object_name = "rentals"

    def get_queryset(self):
        rentals = Rental.objects.all()
        return rentals
    
    def get_permissions(self):
        return get_custom_permissions(self.request)
    
def create_rental(request):
    if request.method == "POST":
        form = RentalCreateForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False) # don't save yet

            #get property and tenant IDs
            property_id = form.cleaned_data['property'].id
            tenant_id = form.cleaned_data['tenant'].id

            rental.property = Property.objects.get(id=property_id)
            rental.tenant = Tenant.objects.get(id=tenant_id)
            rental.lease_duration = rental.lease_end_date - rental.lease_start_date

            # set property status to 'rented' during rental creation
            if rental.property.status != "rented":
                rental.property.status = "rented"
                rental.property.save()

            rental.rent = rental.property.default_rent

            rental.save()
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
    

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class PropertyViewSet(viewsets.ModelViewSet):
    # DRF view handles the API requests
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        return get_custom_permissions(self.request)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_permissions(self):
        return get_custom_permissions(self.request)

class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
            
    def perform_destroy(self, instance):
        instance.property.status = "available"
        instance.property.save()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_permissions(self):
        return get_custom_permissions(self.request)
    
class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

    def get_permissions(self):
        return get_custom_permissions(self.request)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_permissions(self):
        return get_custom_permissions(self.request)
    
class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def get_permissions(self):
        return get_custom_permissions(self.request)

class TotalTransactionsViewSet(viewsets.ModelViewSet):
    queryset = None
    serializer_class = TotalTransactionSerializer

    def get_permissions(self):
        return get_custom_permissions(self.request)
    
    def list(self, request):
        total_payments = Payment.get_total_payments()
        total_expenses = Expense.get_total_expenses()

        serializer = TotalTransactionSerializer(data={
            "total_payments": total_payments,
            "total_expenses": total_expenses,
        })
        
        serializer.is_valid()
        return Response(serializer.data)
    
    # viewset only used for fetching total finiances, DO NOT ALLOW MODIFICATIONS, no 'create' method