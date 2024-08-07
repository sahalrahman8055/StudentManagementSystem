from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):

    refresh = RefreshToken.for_user(user)
    
    if user.is_superuser:
        role = 'admin'
    elif user.groups.filter(name='teacher').exists():
        role = 'teacher'
    else:
        role = 'user'
    
    refresh['role'] = role

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "role": role
    }
