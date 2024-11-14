from pydantic import BaseModel
from datetime import datetime, timezone

class RMAInput(BaseModel):
    name: str
    description: str
    defect: str
    model: str
    color: str
    
    class Config:
        schema_extra = {
            'example': {
                'name': 'Smartphone Screen',
                'description': 'Screen damaged due to impact',
                'defect': 'HARDWARE',
                'model': 'model package',
                'color': 'blue',
            }
        }