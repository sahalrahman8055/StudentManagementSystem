from rest_framework.permissions import BasePermission



class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_staff and request.user.is_superuser)



class isTeacher(BasePermission):
    
    def has_permission(self, request, view):
        try:
            if request.user.teacher:
                return True
        except:
            return False
        
            