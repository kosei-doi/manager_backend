from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from models import schedules as models
from schemas import schedules as schemas
from datetime import datetime, timedelta
from typing import List

def get_schedules(db: Session, start_date: datetime = None, end_date: datetime = None, schedule_type: str = None):
    query = db.query(models.Schedule)
    
    if start_date and end_date:
        query = query.filter(
            or_(
                and_(models.Schedule.start_time >= start_date, models.Schedule.start_time <= end_date),
                and_(models.Schedule.end_time >= start_date, models.Schedule.end_time <= end_date),
                and_(models.Schedule.start_time <= start_date, models.Schedule.end_time >= end_date)
            )
        )
    elif start_date:
        query = query.filter(models.Schedule.start_time >= start_date)
    elif end_date:
        query = query.filter(models.Schedule.end_time <= end_date)
    
    if schedule_type:
        query = query.filter(models.Schedule.schedule_type == schedule_type)
    
    return query.order_by(models.Schedule.start_time.asc()).all()

def get_schedule(db: Session, schedule_id: int):
    return db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()

def create_schedule(db: Session, schedule: schemas.ScheduleCreate):
    db_schedule = models.Schedule(**schedule.model_dump())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def update_schedule(db: Session, schedule_id: int, schedule_update: schemas.ScheduleUpdate):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not db_schedule:
        return None
    
    update_data = schedule_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_schedule, key, value)
    
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def delete_schedule(db: Session, schedule_id: int):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if db_schedule:
        db.delete(db_schedule)
        db.commit()
        return True
    return False

def find_free_time_slots(db: Session, date: datetime, min_duration: int = 30, max_fatigue: int = 10):
    """指定日の空き時間を検索"""
    start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    
    # その日のスケジュールを取得
    schedules = get_schedules(db, start_of_day, end_of_day)
    
    # 基本の活動時間（例：6:00-23:00）
    work_start = start_of_day.replace(hour=6, minute=0)
    work_end = start_of_day.replace(hour=23, minute=0)
    
    # スケジュールを時間順にソート
    sorted_schedules = sorted(schedules, key=lambda x: x.start_time)
    
    free_slots = []
    current_time = work_start
    
    for schedule in sorted_schedules:
        # スケジュールの開始時間までに空き時間があるかチェック
        if current_time < schedule.start_time:
            duration = (schedule.start_time - current_time).total_seconds() / 60
            if duration >= min_duration:
                # 優先度スコアを計算（時間帯と体力を考慮）
                priority_score = calculate_priority_score(current_time, duration, max_fatigue)
                free_slots.append(schemas.FreeTimeSlot(
                    start_time=current_time,
                    end_time=schedule.start_time,
                    duration_minutes=int(duration),
                    priority_score=priority_score
                ))
        
        current_time = max(current_time, schedule.end_time)
    
    # 最後のスケジュール以降の空き時間
    if current_time < work_end:
        duration = (work_end - current_time).total_seconds() / 60
        if duration >= min_duration:
            priority_score = calculate_priority_score(current_time, duration, max_fatigue)
            free_slots.append(schemas.FreeTimeSlot(
                start_time=current_time,
                end_time=work_end,
                duration_minutes=int(duration),
                priority_score=priority_score
            ))
    
    return sorted(free_slots, key=lambda x: x.priority_score, reverse=True)

def calculate_priority_score(time: datetime, duration: float, max_fatigue: int):
    """時間帯と体力を考慮した優先度スコアを計算"""
    hour = time.hour
    
    # 時間帯によるスコア（朝と夕方が高スコア）
    time_score = 1.0
    if 8 <= hour <= 10:  # 朝
        time_score = 1.5
    elif 14 <= hour <= 16:  # 午後
        time_score = 1.3
    elif 19 <= hour <= 21:  # 夜
        time_score = 1.2
    
    # 時間の長さによるスコア
    duration_score = min(duration / 60, 2.0)  # 最大2時間でスコア上限
    
    # 体力残量によるスコア（体力が残っているほど高スコア）
    fatigue_score = 1.0 - (max_fatigue / 10)  # 体力が少ないほど低スコア
    
    return time_score * duration_score * fatigue_score
