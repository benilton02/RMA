from .status_enum import RolesEnum
from functools import wraps


def admin_required(func):
    @wraps(func)
    def wrapper(self, logged_user: dict, *args, **kwargs):
        roles = logged_user['logged_user']['roles']
        is_admin = any(role['value'] == RolesEnum.ADMIN.value for role in roles)

        if not is_admin:
            return {'success': False, 'code': 403, 'detail': 'The user has no permissions to access resources'}
        
        return func(self, logged_user, *args, **kwargs)
    
    return wrapper