from pydantic import BaseModel
from typing import Union, Optional, List
from datetime import datetime
from enum import Enum

class StudyType(str, Enum):
    LECTURE = "lecture"
    ASSIGNMENT = "assignment"
    EXAM = "exam"
    SELF_STUDY = "self_study"

class StudySubject(str, Enum):
    MATH = "math"
    SCIENCE = "science"
    LANGUAGE = "language"
    PROGRAMMING = "programming"
    LITERATURE = "literature"
    HISTORY = "history"
    OTHER = "other"

class StudyBase(BaseModel):
    title: str
    description: Optional[str] = None
    subject: StudySubject
    study_type: StudyType = StudyType.SELF_STUDY
    priority: int = 1
    difficulty: int = 1
    estimated_hours: float = 1.0
    completed_hours: float = 0.0
    deadline: Optional[datetime] = None
    completed: bool = False
    progress_percentage: int = 0

class StudyCreate(StudyBase):
    pass

class StudyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    subject: Optional[StudySubject] = None
    study_type: Optional[StudyType] = None
    priority: Optional[int] = None
    difficulty: Optional[int] = None
    estimated_hours: Optional[float] = None
    completed_hours: Optional[float] = None
    deadline: Optional[datetime] = None
    completed: Optional[bool] = None
    progress_percentage: Optional[int] = None

class Study(StudyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TimetableBase(BaseModel):
    day_of_week: int
    start_time: str
    end_time: str
    subject: StudySubject
    title: str
    room: Optional[str] = None
    teacher: Optional[str] = None

class TimetableCreate(TimetableBase):
    pass

class TimetableUpdate(BaseModel):
    day_of_week: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    subject: Optional[StudySubject] = None
    title: Optional[str] = None
    room: Optional[str] = None
    teacher: Optional[str] = None

class Timetable(TimetableBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StudyRecommendation(BaseModel):
    study: Study
    recommendation_score: float
    reason: str

