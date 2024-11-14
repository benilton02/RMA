from abc import ABC, abstractmethod

from typing import Any

class LogoutUser(ABC):
    """Interface for logout user use case"""

    @abstractmethod
    async def logout(self, refresh_token: str, redis: Any) -> dict[bool]:
        """Logout user"""
        raise NotImplementedError()
