from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from models import meals as models
from schemas import meals as schemas
from crud import meals as crud

router = APIRouter(prefix="/meals", tags=["meals"])

@router.get("/", response_model=List[schemas.Meal])
def read_meals(
    meal_type: Optional[str] = Query(None, description="食事タイプでフィルタ"),
    category: Optional[str] = Query(None, description="カテゴリでフィルタ"),
    is_recommended: Optional[bool] = Query(None, description="おすすめフラグでフィルタ"),
    db: Session = Depends(get_db)
):
    return crud.get_meals(db, meal_type, category, is_recommended)

@router.get("/{meal_id}", response_model=schemas.Meal)
def read_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = crud.get_meal(db, meal_id)
    if meal is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal

@router.post("/", response_model=schemas.Meal)
def create_meal(meal: schemas.MealCreate, db: Session = Depends(get_db)):
    return crud.create_meal(db, meal)

@router.put("/{meal_id}", response_model=schemas.Meal)
def update_meal(meal_id: int, meal: schemas.MealUpdate, db: Session = Depends(get_db)):
    db_meal = crud.update_meal(db, meal_id, meal)
    if db_meal is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    return db_meal

@router.delete("/{meal_id}")
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    success = crud.delete_meal(db, meal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Meal not found")
    return {"detail": "Meal deleted"}

@router.get("/recommendations/", response_model=List[schemas.MealRecommendation])
def get_meal_recommendations(
    current_energy: int = Query(50, description="現在の体力"),
    current_fatigue: int = Query(50, description="現在の疲労度"),
    meal_type: Optional[str] = Query(None, description="食事タイプでフィルタ"),
    db: Session = Depends(get_db)
):
    recommendations = crud.get_meal_recommendations(db, current_energy, current_fatigue, meal_type)
    return [
        schemas.MealRecommendation(
            meal=rec["meal"],
            recommendation_score=rec["recommendation_score"],
            reason=rec["reason"]
        )
        for rec in recommendations
    ]

@router.get("/history/", response_model=List[schemas.MealHistory])
def read_meal_history(
    days: int = Query(7, description="過去何日分の履歴を取得するか"),
    db: Session = Depends(get_db)
):
    return crud.get_meal_history(db, days)

@router.post("/history/", response_model=schemas.MealHistory)
def add_meal_to_history(meal_history: schemas.MealHistoryCreate, db: Session = Depends(get_db)):
    return crud.add_meal_to_history(db, meal_history)

@router.get("/statistics/")
def get_meal_statistics(
    days: int = Query(7, description="過去何日分の統計を取得するか"),
    db: Session = Depends(get_db)
):
    return crud.get_meal_statistics(db, days)
