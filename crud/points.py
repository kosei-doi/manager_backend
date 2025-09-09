from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from datetime import datetime, timedelta
from typing import List
from models import points as models
from schemas import points as schemas

def get_points(db: Session, point_type: str = None, category: str = None, limit: int = 100):
    query = db.query(models.Point)
    if point_type:
        query = query.filter(models.Point.point_type == point_type)
    if category:
        query = query.filter(models.Point.category == category)
    return query.order_by(models.Point.created_at.desc()).limit(limit).all()

def get_point(db: Session, point_id: int):
    return db.query(models.Point).filter(models.Point.id == point_id).first()

def create_point(db: Session, point: schemas.PointCreate):
    # 現在の残高を計算
    current_balance = get_current_balance(db)
    new_balance = current_balance + point.amount if point.point_type == "earned" else current_balance - point.amount
    
    db_point = models.Point(**point.model_dump(), balance_after=new_balance)
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point

def update_point(db: Session, point_id: int, point: schemas.PointUpdate):
    db_point = db.query(models.Point).filter(models.Point.id == point_id).first()
    if db_point:
        update_data = point.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_point, field, value)
        db.commit()
        db.refresh(db_point)
    return db_point

def delete_point(db: Session, point_id: int):
    db_point = db.query(models.Point).filter(models.Point.id == point_id).first()
    if db_point:
        db.delete(db_point)
        db.commit()
        return True
    return False

def get_current_balance(db: Session):
    """現在のポイント残高を取得"""
    latest_point = db.query(models.Point).order_by(models.Point.created_at.desc()).first()
    return latest_point.balance_after if latest_point else 0

def get_point_goals(db: Session, completed: bool = None):
    query = db.query(models.PointGoal)
    if completed is not None:
        query = query.filter(models.PointGoal.completed == completed)
    return query.order_by(models.PointGoal.created_at.desc()).all()

def get_point_goal(db: Session, goal_id: int):
    return db.query(models.PointGoal).filter(models.PointGoal.id == goal_id).first()

def create_point_goal(db: Session, goal: schemas.PointGoalCreate):
    db_goal = models.PointGoal(**goal.model_dump())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def update_point_goal(db: Session, goal_id: int, goal: schemas.PointGoalUpdate):
    db_goal = db.query(models.PointGoal).filter(models.PointGoal.id == goal_id).first()
    if db_goal:
        update_data = goal.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_goal, field, value)
        
        # 目標達成時の処理
        if update_data.get('completed') and not db_goal.completed:
            db_goal.completed_at = datetime.now()
        
        db.commit()
        db.refresh(db_goal)
    return db_goal

def delete_point_goal(db: Session, goal_id: int):
    db_goal = db.query(models.PointGoal).filter(models.PointGoal.id == goal_id).first()
    if db_goal:
        db.delete(db_goal)
        db.commit()
        return True
    return False

def get_point_rewards(db: Session, is_available: bool = None):
    query = db.query(models.PointReward)
    if is_available is not None:
        query = query.filter(models.PointReward.is_available == is_available)
    return query.order_by(models.PointReward.cost.asc()).all()

def get_point_reward(db: Session, reward_id: int):
    return db.query(models.PointReward).filter(models.PointReward.id == reward_id).first()

def create_point_reward(db: Session, reward: schemas.PointRewardCreate):
    db_reward = models.PointReward(**reward.model_dump())
    db.add(db_reward)
    db.commit()
    db.refresh(db_reward)
    return db_reward

def update_point_reward(db: Session, reward_id: int, reward: schemas.PointRewardUpdate):
    db_reward = db.query(models.PointReward).filter(models.PointReward.id == reward_id).first()
    if db_reward:
        update_data = reward.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_reward, field, value)
        db.commit()
        db.refresh(db_reward)
    return db_reward

def delete_point_reward(db: Session, reward_id: int):
    db_reward = db.query(models.PointReward).filter(models.PointReward.id == reward_id).first()
    if db_reward:
        db.delete(db_reward)
        db.commit()
        return True
    return False

def use_point_reward(db: Session, reward_id: int):
    """報酬を使用"""
    db_reward = db.query(models.PointReward).filter(models.PointReward.id == reward_id).first()
    if not db_reward or not db_reward.is_available:
        return None
    
    current_balance = get_current_balance(db)
    if current_balance < db_reward.cost:
        return None
    
    # ポイントを消費
    point_data = {
        "amount": db_reward.cost,
        "point_type": "spent",
        "category": "entertainment",
        "description": f"報酬使用: {db_reward.title}",
        "balance_after": current_balance - db_reward.cost
    }
    
    db_point = models.Point(**point_data)
    db.add(db_point)
    
    # 報酬の使用回数を更新
    db_reward.used_count += 1
    db_reward.is_available = False  # 一度使用したら無効化
    
    db.commit()
    db.refresh(db_point)
    return db_point

def get_point_statistics(db: Session, days: int = 30):
    """ポイント統計を取得"""
    start_date = datetime.now() - timedelta(days=days)
    
    # 期間中のポイント取引
    points = db.query(models.Point).filter(
        models.Point.created_at >= start_date
    ).all()
    
    total_earned = sum(p.amount for p in points if p.point_type == "earned")
    total_spent = sum(p.amount for p in points if p.point_type == "spent")
    current_balance = get_current_balance(db)
    
    # 月間統計
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_points = db.query(models.Point).filter(
        models.Point.created_at >= month_start
    ).all()
    
    monthly_earned = sum(p.amount for p in monthly_points if p.point_type == "earned")
    monthly_spent = sum(p.amount for p in monthly_points if p.point_type == "spent")
    
    # カテゴリ別統計
    category_stats = {}
    for point in points:
        if point.point_type == "earned":
            category_stats[point.category] = category_stats.get(point.category, 0) + point.amount
    
    top_categories = [
        {"category": cat, "amount": amount}
        for cat, amount in sorted(category_stats.items(), key=lambda x: x[1], reverse=True)[:5]
    ]
    
    return {
        "total_earned": total_earned,
        "total_spent": total_spent,
        "current_balance": current_balance,
        "total_transactions": len(points),
        "monthly_earned": monthly_earned,
        "monthly_spent": monthly_spent,
        "top_categories": top_categories
    }
