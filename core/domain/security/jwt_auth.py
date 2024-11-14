from datetime import datetime, timedelta, timezone
from os import getenv
from pathlib import Path
from typing import Dict

import jwt
# from aioredis import Redis
from core.infra.redis.redis_cli import RedisDependency as Redis
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from passlib.context import CryptContext

from core.infra.redis.redis_cli import redis_dependency, get_redis

try:
    dotenv_path = Path('../.env')
    load_dotenv(dotenv_path=dotenv_path)

    SECRET_KEY = getenv('JWT_SECRET_KEY')
    ALGORITHM = getenv('JWT_ALGORITHM', 'HS256')

    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', f'{60 * 24}')
    )
    REFRESH_TOKEN_EXPIRE_MINUTES = int(
        getenv('JWT_REFRESH_TOKEN_EXPIRE_MINUTES', f'{60 * 48}')
    )
except ValueError as error:
    print(error)


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

bearer_scheme = HTTPBearer()


async def get_token(token=Depends(bearer_scheme)) -> str:
    """Fastapi Dependency to get the JWT/Bearer Token"""
    return str(token.credentials)


async def create_jwt_token(data: dict, expires_delta: timedelta) -> str:
    """Creates an JWT Token with `data` and `expire_delta`"""
    data = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    data.update({'exp': expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_data(
    token: str = Depends(get_token), redis: Redis = Depends(redis_dependency)
) -> Dict:
    """Fastapi Dependency to get JWT Data from the User"""
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_revoked = await is_revoked(data=data, redis=redis)
        if user_revoked:
            raise HTTPException(status_code=401, detail='User Revoked')

        revoked_tokens = [
            revoked_token.decode('utf-8')
            for revoked_token in await redis.smembers('revoked_tokens')
        ]

        if token in revoked_tokens:
            raise HTTPException(status_code=401, detail='Token is expired')

    except jwt.exceptions.InvalidTokenError as e:
        if isinstance(e, jwt.exceptions.ExpiredSignatureError):
            raise HTTPException(status_code=401, detail='Token is expired')
        raise HTTPException(status_code=401, detail='Token is invalid')
    return data


async def get_logged_user(
    token: str = Depends(get_token), redis: Redis = Depends(redis_dependency)
) -> Dict:
    """Fastapi Dependency to get JWT Data from the User"""
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if len(data.keys()) == 2:
            raise HTTPException(
                status_code=401,
                detail='Use Access Token instead of Refresh Token',
            )

        revoked_tokens = [
            revoked_token.decode('utf-8')
            for revoked_token in await redis.smembers('revoked_tokens')
        ]
        if token in revoked_tokens:
            raise HTTPException(status_code=401, detail='Token is expired')

    except jwt.exceptions.InvalidTokenError as e:
        if isinstance(e, jwt.exceptions.ExpiredSignatureError):
            raise HTTPException(status_code=401, detail='Token is expired')
        raise HTTPException(status_code=401, detail='Token is invalid')
    return data


async def create_access_token(data: Dict) -> str:
    """Creates an JWT Access Token with `data` and expires after `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`"""
    return await create_jwt_token(
        data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )


async def create_refresh_token(user_id: int, redis: Redis) -> str:
    """Creates an Refresh Token with the `user_id` and needs `redis`"""
    refresh_token_data: Dict = {'user_id': user_id}
    refresh_token: str = await create_jwt_token(
        refresh_token_data, timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    )
    redis.sadd('refresh_tokens', refresh_token)
    return refresh_token


async def invalidate_refresh_token(refresh_token: str, redis: Redis) -> None:
    """Invalidates a Refresh Token"""
    await redis.srem('refresh_tokens', refresh_token)

    access_tokens = [
        access_token.decode('utf-8')
        for access_token in await redis.smembers(refresh_token)
    ]
    for access_token in access_tokens:
        redis.srem(refresh_token, access_token)
        redis.sadd('revoked_tokens', access_token)


async def check_refresh_token(refresh_token: str, redis: Redis) -> bool:
    """Checks if a Refresh Token is valid (in Redis Cache)"""
    data = await get_data(refresh_token, redis)
    if (
        len(data.keys()) != 2
        or 'user_id' not in data.keys()
        or 'exp' not in data.keys()
    ):
        return False

    refresh_tokens = [
        refresh_token.decode('utf-8')
        for refresh_token in await redis.smembers('refresh_tokens')
    ]
    if refresh_token in refresh_tokens:
        return True
    return False


async def generate_tokens(data: Dict, user_id: int, redis: Redis) -> Dict:
    """Generates Access and Refresh Token with `data`, `user_id` and needs redis"""
    access_token: str = await create_access_token(data)
    refresh_token: str = await create_refresh_token(int(user_id), redis)
    redis.sadd(refresh_token, access_token)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer',
    }


async def remove_old_tokens(user_id: int, redis: Redis):
    refresh_tokens = [
        refresh_token.decode('utf-8')
        for refresh_token in await redis.smembers('refresh_tokens')
    ]

    for r_token in refresh_tokens:
        try:
            data = await get_data(r_token, redis)
            if data['user_id'] == user_id:
                await invalidate_refresh_token(
                    refresh_token=r_token, redis=redis
                )
        except HTTPException as e1:
            ...
        except Exception as e2:
            print(e2)


async def revoke_user(
    user_id: int, redis: Redis = Depends(redis_dependency)
) -> bool:

    """Revoke user to system"""
    try:
        redis.sadd(key='revoked_users', member=user_id)
        return True

    except:
        return False


async def grant_user(
    user_id: int, redis: Redis = Depends(redis_dependency)
) -> bool:

    """Grant user to system"""
    try:
        redis.srem(key='revoked_users', member=user_id)
        return True

    except:
        return False


async def revoke_users(
    users_id: list, redis: Redis = Depends(redis_dependency)
) -> bool:

    """Revoke user to system"""
    try:
        redis.sadd('revoked_users', *users_id)
        return True

    except:
        return False


async def grant_users(
    users_id: list, redis: Redis = Depends(redis_dependency)
) -> bool:

    """Grant user to system"""
    try:
        redis.srem('revoked_users', *users_id)
        return True

    except:
        return False


async def is_revoked(data: dict, redis: Redis = Depends(redis_dependency)):
    revoked_users = await redis.smembers('revoked_users')
    tuple_of_ids = tuple(map(int, revoked_users))

    if 'user_id' in data.keys():
        key = 'user_id'

    if 'id' in data.keys():
        key = 'id'

    return data.get(key, False) in tuple_of_ids

async def revoke_device(
    hash_watch: str, redis: Redis = Depends(redis_dependency)
):
    try:
        redis.sadd('revoked_devices', hash_watch)
        return True

    except:
        return False


async def is_device_revoked(
    hash_watch: str, redis: Redis = Depends(redis_dependency)
):
    revoked_devices = await redis.smembers('revoked_devices')
    list_of_revoked_devices = [
        byte.decode('utf-8') for byte in revoked_devices
    ]
    return hash_watch in list_of_revoked_devices


async def remove_device_revoked(
    hash_watch: str, redis: Redis = Depends(redis_dependency)
):
    revoked_devices = await redis.smembers('revoked_devices')
    list_of_revoked_devices = [
        byte.decode('utf-8') for byte in revoked_devices
    ]

    if hash_watch in list_of_revoked_devices:
        redis.srem(key='revoked_devices', member=hash_watch)
        return True

    return False
