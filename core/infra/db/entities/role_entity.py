from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from core.domain.models import Role as RoleModel
from .db_base import Base


class Roles(Base):
    """Roles entity"""

    def __init__(self, role: RoleModel = None):
        super(Roles, self).__init__()
        if role:
            if role.id != 0:
                self.id = role.id
            self.label = role.label
            self.description = role.description
            self.value = role.value

    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    value = Column(String, nullable=False)
    label = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f'Role [value={self.value}]'

    def __eq__(self, other: object) -> bool:
        return self.id == other.id
