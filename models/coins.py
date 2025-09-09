from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum, Float
from sqlalchemy.sql import func
from core.database import Base
import enum

class CoinType(enum.Enum):
    EARNED = "earned"
    SPENT = "spent"
    BONUS = "bonus"
    PENALTY = "penalty"
    EXCHANGE = "exchange"

class CoinCategory(enum.Enum):
    TASK_COMPLETION = "task_completion"
    STUDY_PROGRESS = "study_progress"
    DAILY_LOGIN = "daily_login"
    WEEKLY_GOAL = "weekly_goal"
    MONTHLY_GOAL = "monthly_goal"
    SHOPPING = "shopping"
    GAMING = "gaming"
    ENTERTAINMENT = "entertainment"
    OTHER = "other"

class Coin(Base):
    __tablename__ = "coins"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, default=0)
    coin_type = Column(Enum(CoinType, values_callable=lambda x: [e.value for e in x]), default=CoinType.EARNED)
    category = Column(Enum(CoinCategory, values_callable=lambda x: [e.value for e in x]), default=CoinCategory.OTHER)
    description = Column(Text, nullable=True)
    balance_after = Column(Integer, default=0)  # 取引後の残高
    created_at = Column(DateTime, default=func.now())

class CoinGoal(Base):
    __tablename__ = "coin_goals"

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

class CoinShop(Base):
    __tablename__ = "coin_shop"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    cost = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)
    stock = Column(Integer, default=-1)  # -1は無制限
    used_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class CoinExchange(Base):
    __tablename__ = "coin_exchanges"

    id = Column(Integer, primary_key=True, index=True)
    from_currency = Column(String, default="coin")  # coin, point, etc.
    to_currency = Column(String, default="point")
    from_amount = Column(Integer, default=0)
    to_amount = Column(Integer, default=0)
    exchange_rate = Column(Float, default=1.0)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
