from rest_framework.permissions import BasePermission, SAFE_METHODS
def _is_organizer(user):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
        and user.profile.role == "organizer"
        and user.profile.university_id is not None
    )


class IsOrganizerOrReadOnly(BasePermission):
 
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return _is_organizer(request.user)


class IsOrganizerForEventOrReadOnly(BasePermission):
  
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return _is_organizer(request.user) and obj.university_id == request.user.profile.university_id
