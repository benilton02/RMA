from pydantic import BaseModel


class BaseResponse(BaseModel):
    response: str

    class Config:
        schema_extra = {
            'example': {
                'response': 'server response',
            }
        }
