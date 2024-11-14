from abc import ABC, abstractmethod

from ...domain.models import Role


class RoleRepositoryInterface(ABC):
    """Repository Interface"""

    @classmethod
    @abstractmethod
    def insert_role(cls, role: Role):
        """Insert one object abstract method"""
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def find_Role(cls, role: Role) -> list[Role]:
        """Find Role"""
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def list_role(cls) -> list[Role]:
        """Lind Role"""
        raise NotImplementedError()
