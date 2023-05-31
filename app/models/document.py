from pydantic import BaseModel, UUID4
from typing import Dict
from datetime import datetime

class Document(BaseModel):
    pass

class Projects(BaseModel):
    title: str
    body: Dict