from core.domain.models.role import Role as InternalRole
from core.domain.models.user import User as InternalUser


def get_internal_user(user_data):
    logged_user_roles = []
    for role in user_data['roles']:
        user_role = InternalRole(
            label=role['label'],
            value=role['value'],
            description=role['description'],
            id=role['id'],
        )
        logged_user_roles.append(user_role)

    user = InternalUser(
        full_name=user_data['user_name'],
        email=user_data['email'],
        password='******',
        roles=logged_user_roles,
        id=user_data['id'],
    )
    return user
