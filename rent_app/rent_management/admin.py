from django.contrib import admin

# Register your models here.
from .models import Property, Tenant, Address, ReferencePerson, Rental


admin.site.register(Property)
admin.site.register(Tenant)
admin.site.register(Address)
admin.site.register(ReferencePerson)
admin.site.register(Rental)