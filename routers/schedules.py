from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from schemas import schedules as schemas
from crud import schedules as crud
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/schedules",
    tags=["schedules"]
)

@router.get("/", response_model=List[schemas.Schedule])
def read_schedules(
    db: Session = Depends(get_db),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    schedule_type: Optional[str] = Query(None, description="Schedule type: fixed or flexible")
):
    """スケジュール一覧を取得"""
    start_dt = None
    end_dt = None
    
    if start_date:
        start_dt = datetime.fromisoformat(start_date)
    if end_date:
        end_dt = datetime.fromisoformat(end_date)
    
    return crud.get_schedules(db, start_dt, end_dt, schedule_type)

@router.get("/{schedule_id}", response_model=schemas.Schedule)
def read_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """特定のスケジュールを取得"""
    schedule = crud.get_schedule(db, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

@router.post("/", response_model=schemas.Schedule)
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    """新しいスケジュールを作成"""
    return crud.create_schedule(db, schedule)

@router.put("/{schedule_id}", response_model=schemas.Schedule)
def update_schedule(schedule_id: int, schedule_update: schemas.ScheduleUpdate, db: Session = Depends(get_db)):
    """スケジュールを更新"""
    updated_schedule = crud.update_schedule(db, schedule_id, schedule_update)
    if not updated_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return updated_schedule

@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """スケジュールを削除"""
    success = crud.delete_schedule(db, schedule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"detail": "Schedule deleted"}

@router.patch("/{schedule_id}/complete", response_model=schemas.Schedule)
def complete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """スケジュールを完了にする"""
    schedule = crud.get_schedule(db, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    schedule.completed = True
    schedule.updated_at = datetime.now()
    db.commit()
    db.refresh(schedule)
    return schedule

@router.patch("/{schedule_id}/undo", response_model=schemas.Schedule)
def undo_schedule(schedule_id: int, db: Session = Depends(get_db)):
    """スケジュールの完了を取り消す"""
    schedule = crud.get_schedule(db, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    schedule.completed = False
    schedule.updated_at = datetime.now()
    db.commit()
    db.refresh(schedule)
    return schedule

@router.get("/free-time/{date}", response_model=List[schemas.FreeTimeSlot])
def get_free_time_slots(
    date: str,
    min_duration: int = Query(30, description="Minimum duration in minutes"),
    max_fatigue: int = Query(10, description="Maximum fatigue level"),
    db: Session = Depends(get_db)
):
    """指定日の空き時間を取得"""
    try:
        target_date = datetime.fromisoformat(date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    return crud.find_free_time_slots(db, target_date, min_duration, max_fatigue)

@router.get("/today", response_model=List[schemas.Schedule])
def get_today_schedules(db: Session = Depends(get_db)):
    """今日のスケジュールを取得"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    return crud.get_schedules(db, today, tomorrow)

@router.get("/week", response_model=List[schemas.Schedule])
def get_week_schedules(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """週間スケジュールを取得"""
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    else:
        # 今週の月曜日を開始日とする
        today = datetime.now()
        start_dt = today - timedelta(days=today.weekday())
        start_dt = start_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    
    end_dt = start_dt + timedelta(days=7)
    return crud.get_schedules(db, start_dt, end_dt)
