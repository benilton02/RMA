from dataclasses import dataclass


@dataclass
class Role:
    label: str = ''
    value: str = ''
    description: str = ''
    id: int = 0
