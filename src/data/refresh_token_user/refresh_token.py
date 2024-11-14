from typing import Dict, Type

from aioredis import Redis
from fastapi import HTTPException
from src.domain.use_cases import RefreshToken as RefreshTokenUserInterface
from src.main.schemas.user.user_logged import UserLogged

from core.domain.repositories import UserRepositoryInterface
from core.domain.security.jwt_auth import (
    check_refresh_token,
    generate_tokens,
    get_data,
    invalidate_refresh_token,
)


class RefreshTokenUser(RefreshTokenUserInterface):
    """Login User use case"""

    def __init__(self, user_repository: Type[UserRepositoryInterface]) -> None:
        self.user_repository = user_repository

    async def refresh(
        self, refresh_token: str, redis: Redis
    ) -> dict[bool, UserLogged]:
        validated_entries = True
        data: Dict = {}

        try:
            if not await check_refresh_token(refresh_token, redis):
                raise HTTPException(401, 'Refresh Token Invalid')
            data = await get_data(refresh_token, redis)
        except HTTPException as e:
            if e.detail == 'Token is expired':
                await invalidate_refresh_token(refresh_token, redis)
            return {
                'Success': False,
                'code': e.status_code,
                'detail': e.detail,
            }

        user = self.user_repository.find_user(user={'id': data['user_id']})

        if len(user) != 1:
            return {'Success': False, 'code': 404, 'detail': 'User not found'}

        user = user[0]
        await invalidate_refresh_token(refresh_token, redis)

        user_roles = [
            {
                'id': role.id,
                'value': role.value,
                'label': role.label,
                'description': role.description,
            }
            for role in user.roles
        ]
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
        response = UserLogged(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            access_token=token['access_token'],
            refresh_token=token['refresh_token'],
            token_type=token['token_type'],
            password='******',
            roles=user_roles,
        )

        return {'Success': validated_entries, 'Data': response}
