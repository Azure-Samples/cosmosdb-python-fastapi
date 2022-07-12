from datetime import date
from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4

class ToDoItem(BaseModel):
    id : str = Field(default_factory=uuid4)
    title : str
    description : Optional[str]
    dueDate : date

class UpdateItem(BaseModel):
    id : str
    title : Optional[str]
    description : Optional[str]
    dueDate : Optional[date]