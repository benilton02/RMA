from abc import ABC, abstractmethod
from typing import Type

from core.presentation.helpers import HttpRequest, HttpResponse


class RouteInterface(ABC):
    """Interface to Routes"""

    @abstractmethod
    async def route(self, http_request: Type[HttpRequest]) -> HttpResponse:
        """Route definition"""

        raise NotImplementedError()
