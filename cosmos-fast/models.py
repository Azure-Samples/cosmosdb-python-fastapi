from pydantic import BaseModel
from typing import Optional

class ToDoItem(BaseModel):
    id : str 
    name : Optional[str]
    description : Optional[str]
    isComplete : Optional[bool]

