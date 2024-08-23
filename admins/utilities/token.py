from rest_framework_simplejwt.tokens import RefreshToken
import logging

logger = logging.getLogger(__name__)

def get_tokens_for_user(user):
    try:
        refresh = RefreshToken.for_user(user)
        
        if user.is_superuser:
            role = 'admin'
        elif user.groups.filter(name='teacher').exists():
            role = 'teacher'
        else:
            role = 'user'
        
        refresh['role'] = role  # Add custom claim to the token
        
        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": role
        }
        print(f"Generated tokens for user {user.username}: {tokens}")
        logger.debug(f"Generated tokens for user {user.username}: {tokens}")
        
        return tokens
    except Exception as e:
        logger.error(f"Error generating tokens for user {user.username}: {e}")
        raise e
