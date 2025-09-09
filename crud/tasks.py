from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from models import tasks as models
from schemas import tasks as schemas
from datetime import datetime, timedelta
from typing import List

def get_tasks(db: Session, task_type: str = None, category: str = None, completed: bool = None):
    query = db.query(models.Task)
    
    if task_type:
        query = query.filter(models.Task.type == task_type)
    if category:
        query = query.filter(models.Task.category == category)
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
    
    return query.order_by(models.Task.priority.desc(), models.Task.deadline.asc()).all()

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks_by_deadline(db: Session, days: int = 7):
    """指定日数以内の期限があるタスクを取得"""
    end_date = datetime.now() + timedelta(days=days)
    return db.query(models.Task).filter(
        and_(
            models.Task.deadline.isnot(None),
            models.Task.deadline <= end_date,
            models.Task.completed == False
        )
    ).order_by(models.Task.deadline.asc()).all()

def get_overdue_tasks(db: Session):
    """期限切れのタスクを取得"""
    return db.query(models.Task).filter(
        and_(
            models.Task.deadline.isnot(None),
            models.Task.deadline < datetime.now(),
            models.Task.completed == False
        )
    ).all()

def get_daily_tasks(db: Session):
    """毎日タスクを取得"""
    return db.query(models.Task).filter(models.Task.type == models.TaskType.DAILY).all()

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        return None
    
    update_data = task_update.model_dump(exclude_unset=True)
    
    # 完了状態が変更された場合、completed_atを更新
    if 'completed' in update_data:
        if update_data['completed'] and not db_task.completed:
            update_data['completed_at'] = datetime.now()
        elif not update_data['completed']:
            update_data['completed_at'] = None
    
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False

def get_task_history(db: Session, limit: int = 50):
    """完了したタスクの履歴を取得"""
    return db.query(models.Task).filter(
        models.Task.completed == True
    ).order_by(models.Task.completed_at.desc()).limit(limit).all()

def get_task_statistics(db: Session):
    """タスクの統計情報を取得"""
    total_tasks = db.query(models.Task).count()
    completed_tasks = db.query(models.Task).filter(models.Task.completed == True).count()
    overdue_tasks = len(get_overdue_tasks(db))
    
    return {
        "total": total_tasks,
        "completed": completed_tasks,
        "pending": total_tasks - completed_tasks,
        "overdue": overdue_tasks,
        "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    }
