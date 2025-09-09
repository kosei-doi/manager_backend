from pydantic import BaseModel
from typing import Union, Optional, List
from datetime import datetime
from enum import Enum

class ScheduleType(str, Enum):
    FIXED = "fixed"
    FLEXIBLE = "flexible"

class ScheduleBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    schedule_type: ScheduleType = ScheduleType.FLEXIBLE
    priority: int = 0
    fatigue: int = 0
    completed: bool = False
    category: Optional[str] = None
    location: Optional[str] = None

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    schedule_type: Optional[ScheduleType] = None
    priority: Optional[int] = None
    fatigue: Optional[int] = None
    completed: Optional[bool] = None
    category: Optional[str] = None
    location: Optional[str] = None

class Schedule(ScheduleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class FreeTimeSlot(BaseModel):
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    priority_score: float  # 優先度と体力を考慮したスコア
