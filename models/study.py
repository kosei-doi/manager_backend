from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum, Float
from sqlalchemy.sql import func
from core.database import Base
import enum

class StudyType(enum.Enum):
    LECTURE = "lecture"      # 講義
    ASSIGNMENT = "assignment"  # 課題
    EXAM = "exam"           # 試験
    SELF_STUDY = "self_study"  # 自主学習

class StudySubject(enum.Enum):
    MATH = "math"
    SCIENCE = "science"
    LANGUAGE = "language"
    PROGRAMMING = "programming"
    LITERATURE = "literature"
    HISTORY = "history"
    OTHER = "other"

class Study(Base):
    __tablename__ = "studies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    subject = Column(Enum(StudySubject, values_callable=lambda x: [e.value for e in x]), nullable=False)
    study_type = Column(Enum(StudyType, values_callable=lambda x: [e.value for e in x]), default=StudyType.SELF_STUDY)
    priority = Column(Integer, default=1)  # 1-5 (5が最高)
    difficulty = Column(Integer, default=1)  # 1-5 (5が最高)
    estimated_hours = Column(Float, default=1.0)
    completed_hours = Column(Float, default=0.0)
    deadline = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False)
    progress_percentage = Column(Integer, default=0)  # 0-100
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    completed_at = Column(DateTime, nullable=True)

class Timetable(Base):
    __tablename__ = "timetable"

    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(Integer, nullable=False)  # 0=月曜日, 1=火曜日, ...
    start_time = Column(String, nullable=False)  # "09:00"
    end_time = Column(String, nullable=False)  # "10:30"
    subject = Column(Enum(StudySubject, values_callable=lambda x: [e.value for e in x]), nullable=False)
    title = Column(String, nullable=False)
    room = Column(String, nullable=True)
    teacher = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

