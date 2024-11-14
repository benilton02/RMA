from ..role import Role
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    full_name: str
    email: str
    password: str
    roles: list[Role] = []


    class Config:
        schema_extra = {
            'example': {
                'full_name': 'Mapinguari',
                'email': 'user@email.com',
                'password': '123456',
                'roles': [{
                    'label': 'User',
                    'value': 'USER',
                    'description': 'Basic role. Restricted access',
                }]
            }
        }
