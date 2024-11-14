from ..role import Role
from . import User
from datetime import datetime


class UserLogged(User):
    id: int
    full_name: str
    access_token: str
    refresh_token: str
    token_type: str
    roles: list[Role]

    class Config:
        schema_extra = {
            'example': {
                'id': 1,
                'full_name': 'User Full Name',
                'email': 'user@email.com',
                'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImlkIjo1LCJ1c2VyX25hbWUiOiJ0ZXN0Iiwicm9sZXMiOlsiQURNSU4iXX0sImV4cCI6MTY2MTcxMTc0NH0.lLTIvAqozZS54qogpsjIauag4t-L3SzJvtNM5KyckDg',
                'refresh_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJleHAiOjE2NjE3MzE1NDR9.mex0arRWFcxsMoMAqOjuCkWMJ2V62oAFFr2OXu5Cu7o',
                'token_type': 'bearer',
                'roles': [],
            }
        }
