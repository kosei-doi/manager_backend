from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from schemas import study as schemas
from crud import study as crud

router = APIRouter(
    prefix="/study",
    tags=["study"]
)

# 勉強タスク関連
@router.get("/", response_model=List[schemas.Study])
def read_studies(
    db: Session = Depends(get_db),
    subject: Optional[str] = Query(None, description="Subject filter"),
    study_type: Optional[str] = Query(None, description="Study type filter"),
    completed: Optional[bool] = Query(None, description="Completion status filter")
):
    """勉強タスク一覧を取得"""
    return crud.get_studies(db, subject, study_type, completed)

@router.get("/{study_id}", response_model=schemas.Study)
def read_study(study_id: int, db: Session = Depends(get_db)):
    """特定の勉強タスクを取得"""
    study = crud.get_study(db, study_id)
    if not study:
        raise HTTPException(status_code=404, detail="Study not found")
    return study

@router.post("/", response_model=schemas.Study)
def create_study(study: schemas.StudyCreate, db: Session = Depends(get_db)):
    """新しい勉強タスクを作成"""
    return crud.create_study(db, study)

@router.put("/{study_id}", response_model=schemas.Study)
def update_study(study_id: int, study_update: schemas.StudyUpdate, db: Session = Depends(get_db)):
    """勉強タスクを更新"""
    updated_study = crud.update_study(db, study_id, study_update)
    if not updated_study:
        raise HTTPException(status_code=404, detail="Study not found")
    return updated_study

@router.delete("/{study_id}")
def delete_study(study_id: int, db: Session = Depends(get_db)):
    """勉強タスクを削除"""
    success = crud.delete_study(db, study_id)
    if not success:
        raise HTTPException(status_code=404, detail="Study not found")
    return {"detail": "Study deleted"}

@router.get("/recommendations", response_model=List[schemas.StudyRecommendation])
def get_recommendations(
    limit: int = Query(5, description="Number of recommendations"),
    db: Session = Depends(get_db)
):
    """おすすめの勉強タスクを取得"""
    return crud.get_study_recommendations(db, limit)

@router.get("/history", response_model=List[schemas.Study])
def get_history(
    days: int = Query(30, description="Number of days to look back"),
    db: Session = Depends(get_db)
):
    """勉強履歴を取得"""
    return crud.get_study_history(db, days)

@router.get("/statistics")
def get_statistics(db: Session = Depends(get_db)):
    """勉強統計を取得"""
    return crud.get_study_statistics(db)

# 時間割関連
@router.get("/timetable", response_model=List[schemas.Timetable])
def read_timetable(
    day_of_week: Optional[int] = Query(None, description="Day of week (0=Monday)"),
    db: Session = Depends(get_db)
):
    """時間割を取得"""
    return crud.get_timetable(db, day_of_week)

@router.post("/timetable", response_model=schemas.Timetable)
def create_timetable_entry(timetable: schemas.TimetableCreate, db: Session = Depends(get_db)):
    """時間割エントリを作成"""
    return crud.create_timetable_entry(db, timetable)

@router.put("/timetable/{timetable_id}", response_model=schemas.Timetable)
def update_timetable_entry(timetable_id: int, timetable_update: schemas.TimetableUpdate, db: Session = Depends(get_db)):
    """時間割エントリを更新"""
    updated_timetable = crud.update_timetable_entry(db, timetable_id, timetable_update)
    if not updated_timetable:
        raise HTTPException(status_code=404, detail="Timetable entry not found")
    return updated_timetable

@router.delete("/timetable/{timetable_id}")
def delete_timetable_entry(timetable_id: int, db: Session = Depends(get_db)):
    """時間割エントリを削除"""
    success = crud.delete_timetable_entry(db, timetable_id)
    if not success:
        raise HTTPException(status_code=404, detail="Timetable entry not found")
    return {"detail": "Timetable entry deleted"}

