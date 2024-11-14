from abc import ABC, abstractmethod
from typing import Any
from src.main.schemas.user.user_logged import UserLogged

from core.domain.models import User


class LoginUser(ABC):
    """Interface for login user use case"""

    @abstractmethod
    async def authenticate(
        self, user_name: str, user_password: str, redis: Any, user_agent: str
    ) -> dict[bool, UserLogged]:
        """Login user"""
        raise NotImplementedError()
