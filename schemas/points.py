from pydantic import BaseModel
from typing import Union, Optional, List
from datetime import datetime
from enum import Enum

class PointType(str, Enum):
    EARNED = "earned"
    SPENT = "spent"
    BONUS = "bonus"
    PENALTY = "penalty"

class PointCategory(str, Enum):
    TASK_COMPLETION = "task_completion"
    STUDY_PROGRESS = "study_progress"
    MEAL_HEALTHY = "meal_healthy"
    EXERCISE = "exercise"
    DAILY_GOAL = "daily_goal"
    WEEKLY_GOAL = "weekly_goal"
    SHOPPING = "shopping"
    ENTERTAINMENT = "entertainment"
    OTHER = "other"

class PointBase(BaseModel):
    amount: int = 0
    point_type: PointType = PointType.EARNED
    category: PointCategory = PointCategory.OTHER
    description: Union[str, None] = None
    balance_after: int = 0

class PointCreate(PointBase):
    pass

class PointUpdate(BaseModel):
    amount: Union[int, None] = None
    point_type: Union[PointType, None] = None
    category: Union[PointCategory, None] = None
    description: Union[str, None] = None
    balance_after: Union[int, None] = None

class Point(PointBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PointGoalBase(BaseModel):
    title: str
    description: Union[str, None] = None
    target_amount: int = 0
    current_amount: int = 0
    deadline: Union[datetime, None] = None
    completed: bool = False

class PointGoalCreate(PointGoalBase):
    pass

class PointGoalUpdate(BaseModel):
    title: Union[str, None] = None
    description: Union[str, None] = None
    target_amount: Union[int, None] = None
    current_amount: Union[int, None] = None
    deadline: Union[datetime, None] = None
    completed: Union[bool, None] = None

class PointGoal(PointGoalBase):
    id: int
    completed_at: Union[datetime, None] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PointRewardBase(BaseModel):
    title: str
    description: Union[str, None] = None
    cost: int = 0
    is_available: bool = True
    used_count: int = 0

class PointRewardCreate(PointRewardBase):
    pass

class PointRewardUpdate(BaseModel):
    title: Union[str, None] = None
    description: Union[str, None] = None
    cost: Union[int, None] = None
    is_available: Union[bool, None] = None
    used_count: Union[int, None] = None

class PointReward(PointRewardBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PointStatistics(BaseModel):
    total_earned: int
    total_spent: int
    current_balance: int
    total_transactions: int
    monthly_earned: int
    monthly_spent: int
    top_categories: List[dict]
