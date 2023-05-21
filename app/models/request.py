from pydantic import BaseModel, UUID4


class SessionRequest(BaseModel):
    id: UUID4
    url_response: str