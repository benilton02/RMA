from typing import Type
from core.main.interfaces import RouteInterface as Route
from core.presentation.errors import HttpErrors
from core.presentation.helpers import HttpRequest, HttpResponse
from src.data.rma.rma_use_cases import RMAUseCases

class RMAStepAverageController(Route):
    """User case controller"""

    def __init__(self, rma_use_case: RMAUseCases) -> None:
        self.rma_use_case = rma_use_case

    async def route(self, http_request: Type[HttpRequest]) -> HttpResponse:
        """Http request handler"""
        response = self.rma_use_case.step_average(http_request.body)
        
        if not response['success']:
            return HttpResponse(
                status_code=response['code'],
                body={'error': response['detail']},
                )
        else:
            return HttpResponse(status_code=response['code'], body=response['data'])