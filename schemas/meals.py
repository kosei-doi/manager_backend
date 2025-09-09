from pydantic import BaseModel
from typing import Union, Optional, List
from datetime import datetime
from enum import Enum

class MealType(str, Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"

class MealCategory(str, Enum):
    JAPANESE = "japanese"
    WESTERN = "western"
    CHINESE = "chinese"
    ITALIAN = "italian"
    FAST_FOOD = "fast_food"
    HEALTHY = "healthy"
    OTHER = "other"

class MealBase(BaseModel):
    name: str
    description: Union[str, None] = None
    meal_type: MealType = MealType.LUNCH
    category: MealCategory = MealCategory.OTHER
    calories: int = 0
    protein: float = 0.0
    carbs: float = 0.0
    fat: float = 0.0
    energy_boost: int = 0
    fatigue_reduction: int = 0
    is_recommended: bool = False

class MealCreate(MealBase):
    pass

class MealUpdate(BaseModel):
    name: Union[str, None] = None
    description: Union[str, None] = None
    meal_type: Union[MealType, None] = None
    category: Union[MealCategory, None] = None
    calories: Union[int, None] = None
    protein: Union[float, None] = None
    carbs: Union[float, None] = None
    fat: Union[float, None] = None
    energy_boost: Union[int, None] = None
    fatigue_reduction: Union[int, None] = None
    is_recommended: Union[bool, None] = None

class Meal(MealBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MealHistoryBase(BaseModel):
    meal_id: int
    meal_name: str
    meal_type: MealType
    category: MealCategory
    calories: int = 0
    energy_boost: int = 0
    fatigue_reduction: int = 0

class MealHistoryCreate(MealHistoryBase):
    pass

class MealHistory(MealHistoryBase):
    id: int
    consumed_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class MealRecommendation(BaseModel):
    meal: Meal
    recommendation_score: float
    reason: str
