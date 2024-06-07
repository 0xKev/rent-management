from django.db import models
from django.utils import timezone
from datetime import timedelta
from django import forms
from django.core.exceptions import ValidationError

from django.db.models import Sum

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

    def clean(self):
        # If lease start date greater than lease end date, set end date to start date plus lease duration
        if self.lease_start_date >= self.lease_end_date:
            self.lease_end_date = self.lease_start_date + self.lease_duration

        if self.property.status != "available":
            raise ValidationError("Only available properties can be rented!")

        super().clean()

    def save(self, *args, **kwargs):
        # Used to only set fields only when a new Rental instance is being created
        if not self.pk:
            self.property.status = "rented"

            if not self.rent:
                self.rent = self.property.default_rent
            self.property.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.property.status = "available"
        self.property.save()
        super().delete(*args, **kwargs)


    def __str__(self):
        return f"{self.property.name} - ({self.property.property_type}: {self.tenant.first_name} {self.tenant.last_name}: {self.property.status})"


class Expense(models.Model):
    REPAIR_TYPES = (
        ('general_repair', 'Repair'),
        ('electric_repair', 'Electric Repair'),
        ('other', 'Other')
    )
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, blank=False, null=True)
    owner = models.ForeignKey(User, related_name="expenses", on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    repair_type = models.CharField(max_length=20, choices=REPAIR_TYPES, default='expenses')
    payment_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    date_paid = models.DateField(default=timezone.now().date())
    description = models.CharField(max_length=50, blank=True, null=True)


    @classmethod
    def get_total_expenses(cls):
        total_count = cls.objects.count()
        if total_count == 0:
            return 0
        
        total = Expense.objects.aggregate(Sum("payment_amount"))["payment_amount__sum"]
        return total
        

    def save(self, *args, **kwargs):
        if self.rental:
            self.property = self.rental.property
        super().save(*args, **kwargs)

    def clean(self):
        if not self.property:
            self.property = self.rental.property
        super().clean()

    def __str__(self):
        return f"{self.rental} ({self.repair_type} cost ${self.payment_amount})"

class Payment(models.Model):
    owner = models.ForeignKey(User, related_name="payments", on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    payment_amount = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    date_paid = models.DateField(default=timezone.now().date())
    description = models.CharField(max_length=50, blank=True, null=True)

    @classmethod
    def get_total_payments(cls) -> float:
        """
        Returns total payments as a decimal
        """
        total_count = cls.objects.count()
        if total_count == 0:
            return 0
        
        total = cls.objects.aggregate(Sum("payment_amount"))["payment_amount__sum"]
        return total
    
    def clean(self):
        if not self.property:
            self.property = self.rental.property

        super().clean()

    def __str__(self):
        return f"{self.rental} (profit ${self.payment_amount})"