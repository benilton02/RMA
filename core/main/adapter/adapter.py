import traceback
from typing import Any, Type

from sqlalchemy.exc import IntegrityError

from core.main.interfaces import RouteInterface as Route
from core.presentation.errors import HttpErrors
from core.presentation.helpers import HttpRequest, HttpResponse


async def fastapi_adapter(request, api_route: Type[Route]) -> Any:
    """FastAPI Adapter Pattern
    :param - request: FastAPI request
    :param - api_route: Composite Routes
    """

    http_request = HttpRequest(
        query=request['query'], body=request['body'], header=request['header']
    )

    try:
        response = await api_route.route(http_request)
    except IntegrityError:
        http_error = HttpErrors.error_409()

        return HttpResponse(
            status_code=http_error['status_code'], body=http_error['body']
        )
    except Exception:
        traceback.print_exc()
        http_error = HttpErrors.error_500()

        return HttpResponse(
            status_code=http_error['status_code'], body=http_error['body']
        )

    return response
