from pydantic import BaseModel

class Token(BaseModel):
    code: str