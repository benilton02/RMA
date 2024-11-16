from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import backref, relationship

from core.domain.models import User as UserModel
from .db_base import Base
from .role_entity import Roles
# from .rma_entity import rma_user_association

user_roles_table = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', ForeignKey('users.id', ondelete='CASCADE')),
    Column('role_id', ForeignKey('roles.id', ondelete='CASCADE')),
)


class Users(Base):
    """Users entity"""

    def __init__(self, user: UserModel = None):
        super(Users, self).__init__()
        if user:
            if user.id != 0:
                self.id = user.id
            self.full_name = user.full_name
            self.email = user.email
            self.password = user.password
            for role in user.roles:
                r = Roles(role)
                self.roles.append(r)

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False, unique=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=True, unique=False)
    blocked = Column(Boolean, nullable=False, unique=False, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    roles = relationship(
        'Roles',
        secondary=user_roles_table,
        backref='userin',
    )
    
    status = relationship('UserStatusAssociation', back_populates='user')


    def __repr__(self) -> str:
        return f"""
                User [name={self.full_name}]
                """

    def __eq__(self, other: object) -> bool:
        return self.id == other.id and self.full_name == other.full_name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
