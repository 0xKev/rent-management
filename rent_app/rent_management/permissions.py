from django.conf import settings
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly

class DevelopmentModelPermission(BasePermission):
    def has_permission(self, request, view): # if debug is true, anyone can access, else only authenticated users can access through get_custom_permissions
        return settings.DEBUG
    
def get_custom_permissions(request): # if debug is true, use DevelopmentModelPermission, else use DjangoModelPermissionsOrAnonReadOnly
    if settings.DEBUG:
        return [DevelopmentModelPermission()]
    else:
        return [IsAuthenticatedOrReadOnly()]
    
