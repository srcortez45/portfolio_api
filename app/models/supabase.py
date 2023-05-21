from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class APIResponse(BaseModel):
    data: List[Dict[str, Any]]
    """The data returned by the query."""
    count: Optional[int] = None
    """The number of rows returned."""