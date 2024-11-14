import hashlib
from starlette.datastructures import Headers
from typing import Type, Any
from datetime import datetime
from dateutil import tz
from fastapi import HTTPException
from src.domain.use_cases import LoginUser as LoginUserInterface
from src.main.schemas.user.user_logged import UserLogged

from core.domain.repositories import UserRepositoryInterface
from core.domain.security.jwt_auth import (
    generate_tokens,
    remove_old_tokens,
    is_revoked,
    invalidate_refresh_token,
)
from core.infra.db.entities.user_entity import Users as UsersEntity


class LoginUser(LoginUserInterface):
    """Login User use case"""

    def __init__(self, user_repository: UserRepositoryInterface) -> None:
        self.user_repository = user_repository

    async def authenticate(
        self,
        user_name: str,
        user_password: str,
        redis: Any,
    ) -> dict[bool, UserLogged]:
        response = None
        validated_entries = True
        db_user = self.user_repository.find_user(user={'email': user_name})
        if len(db_user) == 0:
            return {
                'Success': False,
                'Data': {
                    'status_code': 422,
                    'body': {
                        'error': 'Email or Password is not valid on system'
                    },
                },
            }
        user = db_user[0]
        hash_password = hashlib.md5(user_password.encode()).hexdigest()

        if user is None or (user.password != hash_password):
            return {
                'Success': False,
                'Data': {
                    'status_code': 422,
                    'body': {
                        'error': 'Email or Password is not valid on system'
                    },
                },
            }

        if validated_entries:
            user_roles = [
                {
                    'id': role.id,
                    'value': role.value,
                    'label': role.label,
                    'description': role.description,
                }
                for role in user.roles
            ]
            await remove_old_tokens(user.id, redis)

            token = await generate_tokens(
                {
                    'id': user.id,
                    'user_name': user.full_name,
                    'email': user.email,
                    'roles': user_roles,
                },
                user.id,
                redis,
            )

            user_data = {'id': user.id}
            user_revoked = await is_revoked(data=user_data, redis=redis)

            revoked_response = {
                'Success': False,
                'Data': {
                    'status_code': 401,
                    'body': {'error': 'User Revoked'},
                },
            }

            if user_revoked:
                return revoked_response

            if user.blocked:
                try:
                    refresh_token = token['refresh_token']
                    await invalidate_refresh_token(
                        refresh_token=refresh_token, redis=redis
                    )
                    return revoked_response

                finally:
                    pass

            self.user_repository.update_user(user)
            
            response = UserLogged(
                id=user.id,
                full_name=user.full_name,
                email=user.email,
                access_token=token['access_token'],
                refresh_token=token['refresh_token'],
                token_type=token['token_type'],
                roles=user_roles,
                password='******',
            )

        return {'Success': validated_entries, 'Data': response}