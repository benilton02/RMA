from abc import ABC, abstractmethod

from typing import Any
from src.main.schemas.user.user_logged import UserLogged


class RefreshToken(ABC):
    """Interface for Refresh token user use case"""

    @abstractmethod
    async def refresh(
        self, refresh_token: str, redis: Any
    ) -> dict[bool, UserLogged]:
        """Refresh token user"""
        raise NotImplementedError()
