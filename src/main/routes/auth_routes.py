from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from src.main.composer import (
    login_user_composer,
    logout_user_composer,
    refresh_token_user_composer,
)
from src.main.schemas.role.role import Role
from src.main.schemas.user import (
    BaseResponse,
    User,
    UserLogged,
    UserLoginInput,
)

from core.infra.redis.redis_cli import redis_dependency
from core.main.adapter.adapter import fastapi_adapter

auth_router = APIRouter()


@auth_router.post(
    '/login',
    response_description='User',
    response_model=UserLogged,
    tags=['Authtentitacion'],
)
async def login(
    credentials: UserLoginInput,
    request_client: Request,
    redis: Any = Depends(redis_dependency),
):
    """Login user route"""
    request = {
        'query': {
            'user_email': credentials.email,
            'user_password': credentials.password,
        },
        'header': {'headers': request_client.headers},
        'body': {},
    }
    response = await fastapi_adapter(
        request=request, api_route=login_user_composer(redis=redis)
    )

    if response.status_code < 300:
        return response.body

    raise HTTPException(
        detail=response.body['error'], status_code=response.status_code
    )


@auth_router.post(
    '/refresh',
    response_description='User',
    response_model=UserLogged,
    tags=['Authtentitacion'],
)
async def refresh_token(
    refresh_token: str, redis: Any = Depends(redis_dependency)
):
    request = {
        'query': {'refresh_token': refresh_token},
        'header': {},
        'body': {},
    }
    response = await fastapi_adapter(
        request=request, api_route=refresh_token_user_composer(redis=redis)
    )
    if response.status_code < 300:
        return response.body

    raise HTTPException(
        detail=response.body['error'], status_code=response.status_code
    )


@auth_router.post(
    '/logout',
    response_description='success',
    response_model=User,
    tags=['Authtentitacion'],
)
async def logout(refresh_token: str, redis: Any = Depends(redis_dependency)):
    request = {
        'query': {'refresh_token': refresh_token},
        'header': {},
        'body': {},
    }
    response = await fastapi_adapter(
        request=request, api_route=logout_user_composer(redis=redis)
    )

    if response.status_code < 300:
        return response.body

    raise HTTPException(
        detail=response.body['error'], status_code=response.status_code
    )