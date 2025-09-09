from pydantic import BaseModel
from typing import Union, Optional
from datetime import datetime
from enum import Enum

class TaskType(str, Enum):
    DAILY = "daily"
    NORMAL = "normal"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    fatigue: int = 0
    reward: int = 0
    completed: bool = False
    type: TaskType = TaskType.NORMAL
    category: Optional[str] = None
    duration: int = 0  # 分単位
    priority: int = 0

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    fatigue: Optional[int] = None
    reward: Optional[int] = None
    completed: Optional[bool] = None
    type: Optional[TaskType] = None
    category: Optional[str] = None
    duration: Optional[int] = None
    priority: Optional[int] = None

class Task(TaskBase):
    id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
