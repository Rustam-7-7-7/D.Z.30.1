from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    """
    Permission class that checks if the user belongs to the 'Moderators' group.
    """
    def has_permission(self, request, view):
        # Check if the user is in the 'Moderators' group
        return request.user.groups.filter(name='Moderators').exists()

class IsOwner(BasePermission):
    """
    Permission class that checks if the requesting user is the owner of the object.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the object has an 'owner' attribute and if it matches the requesting user
        return obj.owner == request.user
