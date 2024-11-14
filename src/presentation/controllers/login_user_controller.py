from typing import Type

from aioredis import Redis
from src.domain.use_cases import LoginUser

from core.main.interfaces import RouteInterface as Route
from core.presentation.errors import HttpErrors
from core.presentation.helpers import HttpRequest, HttpResponse


class LoginUserController(Route):
    """User case controller"""

    def __init__(self, login_use_case: Type[LoginUser], redis: Redis) -> None:
        self.login_use_case = login_use_case
        self.redis = redis

    async def route(self, http_request: Type[HttpRequest]) -> HttpResponse:
        """Http request handler"""
        response = None

        if http_request.query:
            query_string_params = http_request.query.keys()

            if (
                'user_email' in query_string_params
                and 'user_password' in query_string_params
            ):
                user_name = http_request.query['user_email']
                user_password = http_request.query['user_password']

                response = await self.login_use_case.authenticate(
                    user_name=user_name,
                    user_password=user_password,
                    redis=self.redis,
                )
            else:
                response = {'Success': False, 'Data': None}

            if not response['Success']:
                if 'status_code' in response['Data']:
                    return HttpResponse(
                        status_code=response['Data']['status_code'],
                        body=response['Data']['body'],
                    )
                else:
                    http_error = HttpErrors.error_422()

                    return HttpResponse(
                        status_code=http_error['status_code'],
                        body=http_error['body'],
                    )

            return HttpResponse(status_code=200, body=response['Data'])

        http_error = HttpErrors.error_400()

        return HttpResponse(
            status_code=http_error['status_code'], body=http_error['body']
        )
