from pydantic import BaseModel, IPvAnyAddress, UUID4, AnyHttpUrl
from typing import Optional

class ClientHost(BaseModel):
    id: Optional[UUID4]
    ip: Optional[IPvAnyAddress]
    base_url: Optional[AnyHttpUrl]
