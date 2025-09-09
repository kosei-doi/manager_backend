from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum, Float
from sqlalchemy.sql import func
from core.database import Base
import enum

class MealType(enum.Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"

class MealCategory(enum.Enum):
    JAPANESE = "japanese"
    WESTERN = "western"
    CHINESE = "chinese"
    ITALIAN = "italian"
    FAST_FOOD = "fast_food"
    HEALTHY = "healthy"
    OTHER = "other"

class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    meal_type = Column(Enum(MealType, values_callable=lambda x: [e.value for e in x]), default=MealType.LUNCH)
    category = Column(Enum(MealCategory, values_callable=lambda x: [e.value for e in x]), default=MealCategory.OTHER)
    calories = Column(Integer, default=0)
    protein = Column(Float, default=0.0)
    carbs = Column(Float, default=0.0)
    fat = Column(Float, default=0.0)
    energy_boost = Column(Integer, default=0)  # 体力回復量
    fatigue_reduction = Column(Integer, default=0)  # 疲労軽減量
    is_recommended = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class MealHistory(Base):
    __tablename__ = "meal_history"

    id = Column(Integer, primary_key=True, index=True)
    meal_id = Column(Integer, index=True)
    meal_name = Column(String, index=True)
    meal_type = Column(Enum(MealType, values_callable=lambda x: [e.value for e in x]))
    category = Column(Enum(MealCategory, values_callable=lambda x: [e.value for e in x]))
    calories = Column(Integer, default=0)
    energy_boost = Column(Integer, default=0)
    fatigue_reduction = Column(Integer, default=0)
    consumed_at = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
