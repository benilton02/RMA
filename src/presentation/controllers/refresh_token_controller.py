from typing import Type

from aioredis import Redis
from src.domain.use_cases import RefreshToken

from core.main.interfaces import RouteInterface as Route
from core.presentation.errors import HttpErrors
from core.presentation.helpers import HttpRequest, HttpResponse


class RefreshTokenController(Route):
    """User case controller"""

    def __init__(
        self, refresh_token_use_case: Type[RefreshToken], redis: Redis
    ) -> None:
        self.refresh_token_use_case = refresh_token_use_case
        self.redis = redis

    async def route(self, http_request: Type[HttpRequest]) -> HttpResponse:
        """Http request handler"""
        response = None
        if http_request.query:
            query_string_params = http_request.query.keys()

            if 'refresh_token' in query_string_params:
                refresh_token = http_request.query['refresh_token']
                response = await self.refresh_token_use_case.refresh(
                    refresh_token=refresh_token, redis=self.redis
                )
            else:
                response = {'Success': False, 'Data': None}

            if not response['Success']:
                return HttpResponse(
                    status_code=response['code'],
                    body={'error': response['detail']},
                )

            return HttpResponse(status_code=200, body=response['Data'])

        http_error = HttpErrors.error_400()

        return HttpResponse(
            status_code=http_error['status_code'], body=http_error['body']
        )
