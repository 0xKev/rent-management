from django.db import models
from django.utils import timezone
from datetime import timedelta
from django import forms
from django.core.exceptions import ValidationError

# for token authentication #
from rest_framework.authtoken.models import Token


# Create your models here.
class Address(models.Model):
    class Meta:
        verbose_name_plural = "Addresses"

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
    type = models.CharField(max_length=15, choices=PROPERTY_TYPE_CHOICES)
    other_type = models.CharField(max_length=50, null=True, blank=True) # only show when type is "other" for manual input 
    name = models.CharField(max_length=200)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True) # cascade used to prevent orhpans of address class
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=15, choices=PROPERTY_STATUS, default='available')
    payment_freq = models.CharField(max_length=9, choices=BILLING_CYCLE, default='monthly')
    default_rent = models.DecimalField(max_digits=7, decimal_places=2, default=0.00) # default rent bc could be different depending on contract
    
    def get_payment_freq(self):
        return self.payment_freq
    
    def clean(self): # for data integrity when modifying existing Property objects
        if self.pk is None: # check if clean() is being called during creation, return if true
            return
        if Rental.objects.filter(property=self).exists(): # check if any rental class property references this property 'self'
            if self.status != 'rented':
                raise ValidationError("Status can't be changed while property is rented.")

    def __str__(self):
        return f"{self.name}: {self.type} - {self.get_status_display()} " 
        

class ReferencePerson(models.Model):
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10, blank=True, null=True)
    phone_num = models.CharField(max_length=12, blank=True, null=True)
    email = models.EmailField(max_length=80, blank=True, null=True)
    relationship = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Tenant(models.Model):
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
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    lease_start_date = models.DateField(default=timezone.now())
    lease_end_date = models.DateField(default=timezone.now() + timedelta(days=30))
    lease_duration = models.DurationField(blank=True, null=True, default=timedelta(days=30))
    rent = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    rental_freq = models.CharField(max_length=13, choices=BILLING_CYCLE, default="monthly")
    description = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.property.name} - ({self.property.type}: {self.tenant.first_name} {self.tenant.last_name}: {self.property.status})"
