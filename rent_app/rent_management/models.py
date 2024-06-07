from django.db import models
from django.utils import timezone
from datetime import timedelta
from django import forms
from django.core.exceptions import ValidationError

# for token authentication #
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


# Create your models here.
class Address(models.Model):
    class Meta:
        verbose_name_plural = "Addresses"   
    owner = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    country = models.CharField(max_length=20,)
    state = models.CharField(max_length=20,)
    city = models.CharField(max_length=20,)
    line1 = models.CharField(max_length=50,)
    line2 = models.CharField(max_length=50, blank=True, null=True) 
    zipcode = models.CharField(max_length=10,)

    def __str__(self):
        return f"{self.line1}\n\
                 {self.line2}\n\
                 {self.city} {self.state} {self.zipcode}\n\
                 {self.country}"
# MAKE SURE PROPERTY CAN ONLY BE RENTED ONCE! IF STATUS == RENTED, CAN'T CREATE RENTAL WITH IT
class Property(models.Model):
    class Meta:
        verbose_name_plural = "Properties" # used to have Property show up in admin page as properties and not propertys
        ordering = ["owner"]

    PROPERTY_TYPE_CHOICES = (
        # left is actual value, right is shown value
        ('flat', 'Flat'),
        ('house', 'House'),
        ('condo', 'Condo'),
        ('shop', 'Shop'),
        ('townhouse', 'Townhouse'),
        ('bungalow', 'Bungalow'),
        ('other', 'Other')
    )
    PROPERTY_STATUS = (
        ('available', 'Available'),
        ('under service', 'Under Service'),
        ('unavailable', 'Unavailable'),
        ('sold out', 'Sold Out'),
        ('rented', 'Rented'),
    )
    BILLING_CYCLE = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Anually'),
    )

    owner = models.ForeignKey(User, related_name="properties", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    property_type = models.CharField(max_length=15, choices=PROPERTY_TYPE_CHOICES)
    other_type = models.CharField(max_length=50, null=True, blank=True) # only show when type is "other" for manual input 
    name = models.CharField(max_length=200, unique=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True) # cascade used to prevent orhpans of address class
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=15, choices=PROPERTY_STATUS, default='available')
    payment_freq = models.CharField(max_length=9, choices=BILLING_CYCLE, default='monthly')
    default_rent = models.DecimalField(max_digits=7, decimal_places=2, default=0.00) # default rent bc could be different depending on contract
    
    def get_payment_freq(self):
        return self.payment_freq
    

    def __str__(self):
        return f"{self.name}: {self.property_type} - {self.get_status_display()}" 
        

class ReferencePerson(models.Model):
    owner = models.ForeignKey(User, related_name="reference_persons", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10, blank=True, null=True)
    phone_num = models.CharField(max_length=12, blank=True, null=True)
    email = models.EmailField(max_length=80, blank=True, null=True)
    relationship = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Tenant(models.Model):
    owner = models.ForeignKey(User, related_name="tenants", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    phone_num = models.CharField(max_length=12, blank=True, null=True)
    email = models.CharField(max_length=80, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    reference = models.ForeignKey(ReferencePerson,on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Rental(models.Model):
    BILLING_CYCLE = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Anually'),
    )
    owner = models.ForeignKey(User, related_name="rentals", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    lease_start_date = models.DateField(default=timezone.now)
    lease_end_date = models.DateField(default=timezone.now() + timedelta(days=30))
    lease_duration = models.DurationField(blank=True, null=True, default=timedelta(days=30))
    rent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rental_freq = models.CharField(max_length=13, choices=BILLING_CYCLE, default="monthly")
    description = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.property.name} - ({self.property.type}: {self.tenant.first_name} {self.tenant.last_name}: {self.property.status})"

class Expense(models.Model):
    REPAIR_TYPES = (
        ('repair', 'Repair'),
        ('electric_repair', 'Electric Repair'),
        ('other', 'Other')
    )

    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    repair_type = models.CharField(max_length=20, choices=REPAIR_TYPES, default='repair')
    payment_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    date_paid = models.DateField(default=timezone.now)
    description = models.CharField(max_length=50, blank=True, null=True)

    def get_total_expenses():
        try:
            total = Expense.objects.all().aggregate(sum("payment_amount"))["payment_amount__sum"] or 0
            return total
        except:
            return 0

    def __str__(self):
        return f"{self.rental} (cost ${self.payment_amount})"

class Payment(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    payment_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    date_paid = models.DateField(default=timezone.now)
    description = models.CharField(max_length=50, blank=True, null=True)

    def get_total_payments():
        try:
            total = Payment.objects.all().aggregate(sum(("payment_amount")))["payment_amount__sum"] or 0
            return total
        except:
            return 0
    
    def __str__(self):
        return f"{self.rental} (profit ${self.payment_amount})"