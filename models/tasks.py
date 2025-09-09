from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum
from sqlalchemy.sql import func
from core.database import Base
import enum

class TaskType(enum.Enum):
    DAILY = "daily"
    NORMAL = "normal"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    deadline = Column(DateTime, nullable=True)
    fatigue = Column(Integer, default=0)
    reward = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    type = Column(Enum(TaskType, values_callable=lambda x: [e.value for e in x]), default=TaskType.NORMAL)
    category = Column(String, nullable=True)
    duration = Column(Integer, default=0)  # 分単位
    priority = Column(Integer, default=0)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
