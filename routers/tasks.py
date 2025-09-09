from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from schemas import tasks as schemas
from crud import tasks as crud

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.get("/", response_model=List[schemas.Task])
def read_tasks(
    db: Session = Depends(get_db),
    task_type: Optional[str] = Query(None, description="Task type: daily or normal"),
    category: Optional[str] = Query(None, description="Task category"),
    completed: Optional[bool] = Query(None, description="Filter by completion status")
):
    return crud.get_tasks(db, task_type, category, completed)

@router.get("/daily", response_model=List[schemas.Task])
def read_daily_tasks(db: Session = Depends(get_db)):
    return crud.get_daily_tasks(db)

@router.get("/overdue", response_model=List[schemas.Task])
def read_overdue_tasks(db: Session = Depends(get_db)):
    return crud.get_overdue_tasks(db)

@router.get("/deadline/{days}", response_model=List[schemas.Task])
def read_tasks_by_deadline(days: int, db: Session = Depends(get_db)):
    return crud.get_tasks_by_deadline(db, days)

@router.get("/history", response_model=List[schemas.Task])
def read_task_history(
    limit: int = Query(50, description="Number of history items to return"),
    db: Session = Depends(get_db)
):
    return crud.get_task_history(db, limit)

@router.get("/statistics")
def read_task_statistics(db: Session = Depends(get_db)):
    return crud.get_task_statistics(db)

@router.get("/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)

@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    updated_task = crud.update_task(db, task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.patch("/{task_id}/complete")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task_update = schemas.TaskUpdate(completed=True)
    updated_task = crud.update_task(db, task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task completed successfully"}

@router.patch("/{task_id}/undo")
def undo_task(task_id: int, db: Session = Depends(get_db)):
    task_update = schemas.TaskUpdate(completed=False)
    updated_task = crud.update_task(db, task_id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task undone successfully"}

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = crud.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}

@router.post("/from-history/{task_id}")
def create_task_from_history(task_id: int, db: Session = Depends(get_db)):
    """履歴から新しいタスクを作成"""
    original_task = crud.get_task(db, task_id)
    if not original_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 新しいタスクを作成（完了状態をリセット）
    new_task_data = schemas.TaskCreate(
        title=original_task.title,
        description=original_task.description,
        deadline=None,  # 期限はリセット
        fatigue=original_task.fatigue,
        reward=original_task.reward,
        type=original_task.type,
        category=original_task.category,
        duration=original_task.duration,
        priority=original_task.priority,
        completed=False
    )
    
    return crud.create_task(db, new_task_data)
