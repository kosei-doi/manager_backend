from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum, Float
from sqlalchemy.sql import func
from core.database import Base
import enum

class PointType(enum.Enum):
    EARNED = "earned"
    SPENT = "spent"
    BONUS = "bonus"
    PENALTY = "penalty"

class PointCategory(enum.Enum):
    TASK_COMPLETION = "task_completion"
    STUDY_PROGRESS = "study_progress"
    MEAL_HEALTHY = "meal_healthy"
    EXERCISE = "exercise"
    DAILY_GOAL = "daily_goal"
    WEEKLY_GOAL = "weekly_goal"
    SHOPPING = "shopping"
    ENTERTAINMENT = "entertainment"
    OTHER = "other"

class Point(Base):
    __tablename__ = "points"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, default=0)
    point_type = Column(Enum(PointType, values_callable=lambda x: [e.value for e in x]), default=PointType.EARNED)
    category = Column(Enum(PointCategory, values_callable=lambda x: [e.value for e in x]), default=PointCategory.OTHER)
    description = Column(Text, nullable=True)
    balance_after = Column(Integer, default=0)  # 取引後の残高
    created_at = Column(DateTime, default=func.now())

class PointGoal(Base):
    __tablename__ = "point_goals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    target_amount = Column(Integer, default=0)
    current_amount = Column(Integer, default=0)
    deadline = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class PointReward(Base):
    __tablename__ = "point_rewards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    cost = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)
    used_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
