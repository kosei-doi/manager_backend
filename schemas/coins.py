from pydantic import BaseModel
from typing import Union, Optional, List
from datetime import datetime
from enum import Enum

class CoinType(str, Enum):
    EARNED = "earned"
    SPENT = "spent"
    BONUS = "bonus"
    PENALTY = "penalty"
    EXCHANGE = "exchange"

class CoinCategory(str, Enum):
    TASK_COMPLETION = "task_completion"
    STUDY_PROGRESS = "study_progress"
    DAILY_LOGIN = "daily_login"
    WEEKLY_GOAL = "weekly_goal"
    MONTHLY_GOAL = "monthly_goal"
    SHOPPING = "shopping"
    GAMING = "gaming"
    ENTERTAINMENT = "entertainment"
    OTHER = "other"

class CoinBase(BaseModel):
    amount: int = 0
    coin_type: CoinType = CoinType.EARNED
    category: CoinCategory = CoinCategory.OTHER
    description: Union[str, None] = None
    balance_after: int = 0

class CoinCreate(CoinBase):
    pass

class CoinUpdate(BaseModel):
    amount: Union[int, None] = None
    coin_type: Union[CoinType, None] = None
    category: Union[CoinCategory, None] = None
    description: Union[str, None] = None
    balance_after: Union[int, None] = None

class Coin(CoinBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CoinGoalBase(BaseModel):
    title: str
    description: Union[str, None] = None
    target_amount: int = 0
    current_amount: int = 0
    deadline: Union[datetime, None] = None
    completed: bool = False

class CoinGoalCreate(CoinGoalBase):
    pass

class CoinGoalUpdate(BaseModel):
    title: Union[str, None] = None
    description: Union[str, None] = None
    target_amount: Union[int, None] = None
    current_amount: Union[int, None] = None
    deadline: Union[datetime, None] = None
    completed: Union[bool, None] = None

class CoinGoal(CoinGoalBase):
    id: int
    completed_at: Union[datetime, None] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CoinShopBase(BaseModel):
    title: str
    description: Union[str, None] = None
    cost: int = 0
    is_available: bool = True
    stock: int = -1
    used_count: int = 0

class CoinShopCreate(CoinShopBase):
    pass

class CoinShopUpdate(BaseModel):
    title: Union[str, None] = None
    description: Union[str, None] = None
    cost: Union[int, None] = None
    is_available: Union[bool, None] = None
    stock: Union[int, None] = None
    used_count: Union[int, None] = None

class CoinShop(CoinShopBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CoinExchangeBase(BaseModel):
    from_currency: str = "coin"
    to_currency: str = "point"
    from_amount: int = 0
    to_amount: int = 0
    exchange_rate: float = 1.0
    description: Union[str, None] = None

class CoinExchangeCreate(CoinExchangeBase):
    pass

class CoinExchange(CoinExchangeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CoinStatistics(BaseModel):
    total_earned: int
    total_spent: int
    current_balance: int
    total_transactions: int
    monthly_earned: int
    monthly_spent: int
    top_categories: List[dict]
