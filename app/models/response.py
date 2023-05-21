from pydantic import BaseModel
from typing import Optional

class ResponseAPI(BaseModel):
    status: str
    code: int
    message: str
    result: str

class GenerateURLResponse(BaseModel):
    url: Optional[str]
    active_session: bool

class SessionResponse(BaseModel):
    session_type: str
    message: str




