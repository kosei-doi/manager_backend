from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from models import points as models
from schemas import points as schemas
from crud import points as crud

router = APIRouter(prefix="/points", tags=["points"])

# ポイント取引関連
@router.get("/", response_model=List[schemas.Point])
def read_points(
    point_type: Optional[str] = Query(None, description="ポイントタイプでフィルタ"),
    category: Optional[str] = Query(None, description="カテゴリでフィルタ"),
    limit: int = Query(100, description="取得件数"),
    db: Session = Depends(get_db)
):
    return crud.get_points(db, point_type, category, limit)

@router.get("/{point_id}", response_model=schemas.Point)
def read_point(point_id: int, db: Session = Depends(get_db)):
    point = crud.get_point(db, point_id)
    if point is None:
        raise HTTPException(status_code=404, detail="Point not found")
    return point

@router.post("/", response_model=schemas.Point)
def create_point(point: schemas.PointCreate, db: Session = Depends(get_db)):
    return crud.create_point(db, point)

@router.put("/{point_id}", response_model=schemas.Point)
def update_point(point_id: int, point: schemas.PointUpdate, db: Session = Depends(get_db)):
    db_point = crud.update_point(db, point_id, point)
    if db_point is None:
        raise HTTPException(status_code=404, detail="Point not found")
    return db_point

@router.delete("/{point_id}")
def delete_point(point_id: int, db: Session = Depends(get_db)):
    success = crud.delete_point(db, point_id)
    if not success:
        raise HTTPException(status_code=404, detail="Point not found")
    return {"detail": "Point deleted"}

@router.get("/balance/")
def get_current_balance(db: Session = Depends(get_db)):
    return {"balance": crud.get_current_balance(db)}

# ポイント目標関連
@router.get("/goals/", response_model=List[schemas.PointGoal])
def read_point_goals(
    completed: Optional[bool] = Query(None, description="完了状態でフィルタ"),
    db: Session = Depends(get_db)
):
    return crud.get_point_goals(db, completed)

@router.get("/goals/{goal_id}", response_model=schemas.PointGoal)
def read_point_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = crud.get_point_goal(db, goal_id)
    if goal is None:
        raise HTTPException(status_code=404, detail="Point goal not found")
    return goal

@router.post("/goals/", response_model=schemas.PointGoal)
def create_point_goal(goal: schemas.PointGoalCreate, db: Session = Depends(get_db)):
    return crud.create_point_goal(db, goal)

@router.put("/goals/{goal_id}", response_model=schemas.PointGoal)
def update_point_goal(goal_id: int, goal: schemas.PointGoalUpdate, db: Session = Depends(get_db)):
    db_goal = crud.update_point_goal(db, goal_id, goal)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Point goal not found")
    return db_goal

@router.delete("/goals/{goal_id}")
def delete_point_goal(goal_id: int, db: Session = Depends(get_db)):
    success = crud.delete_point_goal(db, goal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Point goal not found")
    return {"detail": "Point goal deleted"}

# ポイント報酬関連
@router.get("/rewards/", response_model=List[schemas.PointReward])
def read_point_rewards(
    is_available: Optional[bool] = Query(None, description="利用可能状態でフィルタ"),
    db: Session = Depends(get_db)
):
    return crud.get_point_rewards(db, is_available)

@router.get("/rewards/{reward_id}", response_model=schemas.PointReward)
def read_point_reward(reward_id: int, db: Session = Depends(get_db)):
    reward = crud.get_point_reward(db, reward_id)
    if reward is None:
        raise HTTPException(status_code=404, detail="Point reward not found")
    return reward

@router.post("/rewards/", response_model=schemas.PointReward)
def create_point_reward(reward: schemas.PointRewardCreate, db: Session = Depends(get_db)):
    return crud.create_point_reward(db, reward)

@router.put("/rewards/{reward_id}", response_model=schemas.PointReward)
def update_point_reward(reward_id: int, reward: schemas.PointRewardUpdate, db: Session = Depends(get_db)):
    db_reward = crud.update_point_reward(db, reward_id, reward)
    if db_reward is None:
        raise HTTPException(status_code=404, detail="Point reward not found")
    return db_reward

@router.delete("/rewards/{reward_id}")
def delete_point_reward(reward_id: int, db: Session = Depends(get_db)):
    success = crud.delete_point_reward(db, reward_id)
    if not success:
        raise HTTPException(status_code=404, detail="Point reward not found")
    return {"detail": "Point reward deleted"}

@router.post("/rewards/{reward_id}/use")
def use_point_reward(reward_id: int, db: Session = Depends(get_db)):
    result = crud.use_point_reward(db, reward_id)
    if result is None:
        raise HTTPException(status_code=400, detail="Cannot use reward")
    return {"detail": "Reward used successfully", "point_transaction": result}

# 統計関連
@router.get("/statistics/")
def get_point_statistics(
    days: int = Query(30, description="過去何日分の統計を取得するか"),
    db: Session = Depends(get_db)
):
    return crud.get_point_statistics(db, days)
