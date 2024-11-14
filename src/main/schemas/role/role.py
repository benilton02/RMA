from pydantic import BaseModel


class Role(BaseModel):
    value: str
    label: str
    description: str = ''
    id: int = 0

    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'value': 'USER',
                'label': 'USER',
                'description': 'basic',
            }
        }
