from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from crud import tasks as crud
from datetime import datetime, timedelta
import json

router = APIRouter(
    prefix="/reminders",
    tags=["reminders"]
)

@router.get("/upcoming")
def get_upcoming_reminders(
    db: Session = Depends(get_db),
    hours: int = Query(24, description="Hours ahead to check for reminders")
):
    """指定時間内のリマインダーを取得"""
    now = datetime.now()
    end_time = now + timedelta(hours=hours)
    
    # 期限があるタスクを取得
    tasks_with_deadline = crud.get_tasks_by_deadline(db, days=hours//24)
    
    reminders = []
    for task in tasks_with_deadline:
        if task.deadline:
            # 睡眠時間を考慮したリマインダー時間を計算
            # 予定睡眠時間から10時間前、または期限の30分前の早い方
            sleep_time = datetime.now().replace(hour=23, minute=0, second=0, microsecond=0)  # 23:00を仮定
            reminder_time_1 = sleep_time - timedelta(hours=10)  # 睡眠10時間前
            reminder_time_2 = task.deadline - timedelta(minutes=30)  # 期限30分前
            
            reminder_time = min(reminder_time_1, reminder_time_2)
            
            if now <= reminder_time <= end_time:
                reminders.append({
                    "task_id": task.id,
                    "task_title": task.title,
                    "deadline": task.deadline.isoformat(),
                    "reminder_time": reminder_time.isoformat(),
                    "type": "deadline_reminder",
                    "message": f"タスク「{task.title}」の期限が近づいています"
                })
    
    return reminders

@router.get("/overdue")
def get_overdue_reminders(db: Session = Depends(get_db)):
    """期限切れのリマインダーを取得"""
    overdue_tasks = crud.get_overdue_tasks(db)
    
    reminders = []
    for task in overdue_tasks:
        reminders.append({
            "task_id": task.id,
            "task_title": task.title,
            "deadline": task.deadline.isoformat() if task.deadline else None,
            "overdue_hours": int((datetime.now() - task.deadline).total_seconds() / 3600) if task.deadline else 0,
            "type": "overdue_reminder",
            "message": f"タスク「{task.title}」の期限が過ぎています"
        })
    
    return reminders

@router.get("/daily-reset")
def get_daily_reset_reminders(db: Session = Depends(get_db)):
    """毎日タスクのリセットリマインダー"""
    daily_tasks = crud.get_daily_tasks(db)
    
    reminders = []
    for task in daily_tasks:
        if task.completed:
            # 完了した毎日タスクのリセットリマインダー
            reminders.append({
                "task_id": task.id,
                "task_title": task.title,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "type": "daily_reset",
                "message": f"毎日タスク「{task.title}」をリセットできます"
            })
    
    return reminders
