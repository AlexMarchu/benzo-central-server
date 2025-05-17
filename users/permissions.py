from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'manager_profile')

class IsManagerOfGasStation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not hasattr(request.user, 'manager_profile'):
            return False
        return obj.gas_station == request.user.manager_profile.gas_station