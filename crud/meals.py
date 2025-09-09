from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from datetime import datetime, timedelta
from typing import List
from models import meals as models
from schemas import meals as schemas

def get_meals(db: Session, meal_type: str = None, category: str = None, is_recommended: bool = None):
    query = db.query(models.Meal)
    if meal_type:
        query = query.filter(models.Meal.meal_type == meal_type)
    if category:
        query = query.filter(models.Meal.category == category)
    if is_recommended is not None:
        query = query.filter(models.Meal.is_recommended == is_recommended)
    return query.order_by(models.Meal.name.asc()).all()

def get_meal(db: Session, meal_id: int):
    return db.query(models.Meal).filter(models.Meal.id == meal_id).first()

def create_meal(db: Session, meal: schemas.MealCreate):
    db_meal = models.Meal(**meal.model_dump())
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal

def update_meal(db: Session, meal_id: int, meal: schemas.MealUpdate):
    db_meal = db.query(models.Meal).filter(models.Meal.id == meal_id).first()
    if db_meal:
        update_data = meal.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_meal, field, value)
        db.commit()
        db.refresh(db_meal)
    return db_meal

def delete_meal(db: Session, meal_id: int):
    db_meal = db.query(models.Meal).filter(models.Meal.id == meal_id).first()
    if db_meal:
        db.delete(db_meal)
        db.commit()
        return True
    return False

def get_meal_recommendations(db: Session, current_energy: int = 50, current_fatigue: int = 50, meal_type: str = None):
    """体力と疲労度に基づいて食事を推薦"""
    query = db.query(models.Meal)
    
    if meal_type:
        query = query.filter(models.Meal.meal_type == meal_type)
    
    meals = query.all()
    recommendations = []
    
    for meal in meals:
        score = calculate_recommendation_score(meal, current_energy, current_fatigue)
        reason = get_recommendation_reason(meal, current_energy, current_fatigue)
        
        recommendations.append({
            "meal": meal,
            "recommendation_score": score,
            "reason": reason
        })
    
    # スコア順にソート
    recommendations.sort(key=lambda x: x["recommendation_score"], reverse=True)
    return recommendations

def calculate_recommendation_score(meal: models.Meal, current_energy: int, current_fatigue: int) -> float:
    """食事の推薦スコアを計算"""
    score = 0.0
    
    # 体力が低い場合は体力回復を重視
    if current_energy < 30:
        score += meal.energy_boost * 2.0
    elif current_energy < 60:
        score += meal.energy_boost * 1.5
    else:
        score += meal.energy_boost * 0.5
    
    # 疲労が高い場合は疲労軽減を重視
    if current_fatigue > 70:
        score += meal.fatigue_reduction * 2.0
    elif current_fatigue > 40:
        score += meal.fatigue_reduction * 1.5
    else:
        score += meal.fatigue_reduction * 0.5
    
    # カロリーも考慮（適度なカロリーを推奨）
    if 300 <= meal.calories <= 800:
        score += 10
    elif 200 <= meal.calories <= 1000:
        score += 5
    
    # 栄養バランスを考慮
    if meal.protein > 0 and meal.carbs > 0 and meal.fat > 0:
        score += 5
    
    return score

def get_recommendation_reason(meal: models.Meal, current_energy: int, current_fatigue: int) -> str:
    """推薦理由を生成"""
    reasons = []
    
    if current_energy < 30 and meal.energy_boost > 20:
        reasons.append("体力回復に効果的")
    elif current_energy < 60 and meal.energy_boost > 10:
        reasons.append("体力を回復")
    
    if current_fatigue > 70 and meal.fatigue_reduction > 20:
        reasons.append("疲労軽減に効果的")
    elif current_fatigue > 40 and meal.fatigue_reduction > 10:
        reasons.append("疲労を軽減")
    
    if 300 <= meal.calories <= 800:
        reasons.append("適度なカロリー")
    
    if meal.protein > 20:
        reasons.append("タンパク質豊富")
    
    if not reasons:
        reasons.append("バランスの良い食事")
    
    return "、".join(reasons)

def get_meal_history(db: Session, days: int = 7):
    """食事履歴を取得"""
    start_date = datetime.now() - timedelta(days=days)
    return db.query(models.MealHistory).filter(
        models.MealHistory.consumed_at >= start_date
    ).order_by(models.MealHistory.consumed_at.desc()).all()

def add_meal_to_history(db: Session, meal_history: schemas.MealHistoryCreate):
    """食事履歴に追加"""
    db_meal_history = models.MealHistory(**meal_history.model_dump())
    db.add(db_meal_history)
    db.commit()
    db.refresh(db_meal_history)
    return db_meal_history

def get_meal_statistics(db: Session, days: int = 7):
    """食事統計を取得"""
    start_date = datetime.now() - timedelta(days=days)
    
    # 期間中の食事履歴
    history = db.query(models.MealHistory).filter(
        models.MealHistory.consumed_at >= start_date
    ).all()
    
    if not history:
        return {
            "total_meals": 0,
            "total_calories": 0,
            "total_energy_boost": 0,
            "total_fatigue_reduction": 0,
            "avg_calories_per_meal": 0,
            "most_consumed_category": None,
            "most_consumed_type": None
        }
    
    total_meals = len(history)
    total_calories = sum(h.calories for h in history)
    total_energy_boost = sum(h.energy_boost for h in history)
    total_fatigue_reduction = sum(h.fatigue_reduction for h in history)
    
    # 最も消費されたカテゴリ
    category_counts = {}
    type_counts = {}
    for h in history:
        category_counts[h.category] = category_counts.get(h.category, 0) + 1
        type_counts[h.meal_type] = type_counts.get(h.meal_type, 0) + 1
    
    most_consumed_category = max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else None
    most_consumed_type = max(type_counts.items(), key=lambda x: x[1])[0] if type_counts else None
    
    return {
        "total_meals": total_meals,
        "total_calories": total_calories,
        "total_energy_boost": total_energy_boost,
        "total_fatigue_reduction": total_fatigue_reduction,
        "avg_calories_per_meal": total_calories / total_meals if total_meals > 0 else 0,
        "most_consumed_category": most_consumed_category,
        "most_consumed_type": most_consumed_type
    }
