from pydantic import BaseModel
from typing import List, Optional

from enum import Enum
from pydantic import BaseModel

class ContentType(str, Enum):
    name='TITLE'
    profession='SUBTITLE'
    content='NORMAL_TEXT'
    HEADING_1=''
    HEADING_2=''



class Content(BaseModel):
    ke = int
    end_index = int
    #paragraphs = 

class Body(BaseModel):
    content = List[Content]
