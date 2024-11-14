from pydantic import BaseModel, EmailStr


class UserLoginInput(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            'example': {'email': 'user@email.com', 'password': '123456'}
        }
