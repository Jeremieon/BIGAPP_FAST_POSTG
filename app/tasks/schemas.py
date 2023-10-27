from typing import List,Union
from pydantic import BaseModel
from datetime import datetime

# Define SQLAlchemy Models
class TaskBase(BaseModel):
    title: str
    description: str

class TaskCreate(TaskBase):
    owner_id: int

class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int

class TaskDB(Task):
    is_completed: bool 

class TokenData(BaseModel):
    id:int
    username: Union[str, None] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TaskUpdate(BaseModel):
    title: str
    description: str
    completed: bool

class TaskSchema(BaseModel):
    id: int
    title: str
    description: str