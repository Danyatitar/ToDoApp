from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class UserModelRegister(BaseModel):
    name: str
    email: str
    password: str

class UserModelLogin(BaseModel):
    email: str
    password: str
    

class UserUpdate(BaseModel):
    name: str
    
class UserCreateAdmin(BaseModel):
    name: str
    role: str
    email:str
    password: str
    
class UserUpdateAdmin(BaseModel):
    name: str
    role: str
    email:str


class TaskStatus(str, Enum):
    in_progress = 'in progress'
    completed = 'completed'
    waiting = 'waiting'

class TaskCreate(BaseModel):
    title: str = Field(min_length=4)
    description: str = ""
    deadline: str
    status: TaskStatus
    category_id: Optional[str] = None

class TaskCreateAdmin(BaseModel):
    title: str = Field(min_length=4)
    description: str = ""
    deadline: str
    status: TaskStatus
    category_id: Optional[str] = None
    user_id: str = None
    
    
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=4)
    description: str = None
    deadline: Optional[str] = None
    status: Optional[TaskStatus] = None
    category_id: Optional[str] = None

class TaskUpdateAdmin(BaseModel):
    title: Optional[str] = Field(None, min_length=4)
    description: str = None
    deadline: Optional[str] = None
    status: Optional[TaskStatus] = None
    category_id: Optional[str] = None
    user_id: str = None
    


class CategoryCreate(BaseModel):
    name: str

class CategoryUpdateAdmin(BaseModel):
    name: str
    user_id: str = None
    