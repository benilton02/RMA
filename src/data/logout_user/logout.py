import email
from typing import Type

from aioredis import Redis
from fastapi import HTTPException
from src.domain.use_cases import LogoutUser as LogoutUserInterface

from core.domain.security.jwt_auth import (
    check_refresh_token,
    get_data,
    invalidate_refresh_token,
)


class LogoutUser(LogoutUserInterface):
    """Login User use case"""

    def __init__(self) -> None:
        pass

    async def logout(self, refresh_token: str, redis: Redis) -> dict[bool]:
        validated_entries = True
        try:
            validated_entries = await check_refresh_token(refresh_token, redis)
            print('check', validated_entries)
            if not validated_entries:
                raise HTTPException(401, 'Refresh Token Invalid')
            data = await get_data(refresh_token, redis)
        except HTTPException as e:
            if e.detail == 'Token is expired':
                await invalidate_refresh_token(refresh_token, redis)

            return {
                'Success': validated_entries,
                'code': e.status_code,
                'detail': e.detail,
            }
        await invalidate_refresh_token(refresh_token, redis)

        return {'Success': validated_entries}
