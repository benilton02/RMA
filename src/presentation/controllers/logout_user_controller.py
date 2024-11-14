from typing import Type

from aioredis import Redis
from src.domain.use_cases import LogoutUser
from src.main.schemas.user import User

from core.main.interfaces import RouteInterface as Route
from core.presentation.errors import HttpErrors
from core.presentation.helpers import HttpRequest, HttpResponse


class LogoutUserController(Route):
    """User case controller"""

    def __init__(
        self, logout_use_case: Type[LogoutUser], redis: Redis
    ) -> None:
        self.logout_use_case = logout_use_case
        self.redis = redis

    async def route(self, http_request: Type[HttpRequest]) -> HttpResponse:
        """Http request handler"""
        response = None

        if http_request.query:
            query_string_params = http_request.query.keys()

            if 'refresh_token' in query_string_params:
                refresh_token = http_request.query['refresh_token']
                response = await self.logout_use_case.logout(
                    refresh_token=refresh_token, redis=self.redis
                )
            else:
                response = {'Success': False, 'Data': None}

            if response['Success']:
                annonymous_user = User(
                    full_name='', email='', password=''
                )
                return HttpResponse(status_code=200, body=annonymous_user)
            else:
                return HttpResponse(
                    status_code=response['code'],
                    body={'error': response['detail']},
                )

        http_error = HttpErrors.error_400()

        return HttpResponse(
            status_code=http_error['status_code'], body=http_error['body']
        )
