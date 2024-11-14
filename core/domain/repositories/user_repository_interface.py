from abc import ABC, abstractmethod

from ...domain.models import User as UserModel
from ...infra.db.entities import Users


class UserRepositoryInterface(ABC):
    """Repository Interface"""

    @classmethod
    @abstractmethod
    def insert_user(cls, user: UserModel) -> Users:
        """Insert one object abstract method"""
        raise NotImplementedError()

    @classmethod
    def update_user(cls, user: UserModel) -> Users:
        """Update one object abstract method"""
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def find_user(cls, user: dict) -> list[Users]:
        """Find user"""
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def full_text_search(cls, user: dict) -> list[Users]:
        """Find user"""
        raise NotImplementedError()
