from pydantic import BaseModel
from datetime import datetime, timezone
from uuid import uuid4

class RMAInput(BaseModel):
    name: str
    description: str
    defect: str
    model: str
    color: str
    serial_number: str
    
    class Config:
        schema_extra = {
            'example': {
                'name': 'Smartphone Screen',
                'description': 'Screen damaged due to impact',
                'defect': 'HARDWARE',
                'model': 'model package',
                'color': 'blue',
                'serial_number': uuid4().hex
            }
        }