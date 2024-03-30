from django.contrib import admin

# Register your models here.
from .models import *


# only used to check everything works as expected, 
# prob better way to register each class instead of manually

admin.site.register(Property)
admin.site.register(Tenant)
admin.site.register(Address)
admin.site.register(ReferencePerson)
admin.site.register(Rental)
admin.site.register(Expense)
admin.site.register(Payment)
