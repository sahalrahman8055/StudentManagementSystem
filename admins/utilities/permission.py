from rest_framework.permissions import BasePermission


from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_staff and request.user.is_superuser

class IsTeacher(BasePermission):
    """
    Allows access only to users who are teachers.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'teacher') and request.user.teacher


class IsAdminOrTeacher(BasePermission):
    """
    Allows access only to admin users or teachers.
    """
    def has_permission(self, request, view):
        is_admin = request.user.is_staff and request.user.is_superuser
        is_teacher = hasattr(request.user, 'teacher') and request.user.teacher
        return is_admin or is_teacher




# class IsAdminUser(BasePermission):
#     """
#     Allows access only to admin users.
#     """

#     def has_permission(self, request, view):
#         return bool(request.user.is_staff and request.user.is_superuser)


# class isTeacher(BasePermission):

#     def has_permission(self, request, view):
#         try:
#             if request.user.teacher:
#                 return True
#         except:
#             return False
