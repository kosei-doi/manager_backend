from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum
from sqlalchemy.sql import func
from core.database import Base
import enum

class ScheduleType(enum.Enum):
    FIXED = "fixed"      # 固定予定（学校、バイトなど）
    FLEXIBLE = "flexible"  # 急な予定

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    schedule_type = Column(Enum(ScheduleType, values_callable=lambda x: [e.value for e in x]), default=ScheduleType.FLEXIBLE)
    priority = Column(Integer, default=0)
    fatigue = Column(Integer, default=0)  # 体力消費
    completed = Column(Boolean, default=False)
    category = Column(String, nullable=True)  # 学校、バイト、個人など
    location = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
