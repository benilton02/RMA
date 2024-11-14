from dataclasses import dataclass
from datetime import datetime

from .role import Role


@dataclass
class User:
    full_name: str
    email: str
    password: str
    roles: list[Role]
    id: int = 0
    blocked: bool = False
