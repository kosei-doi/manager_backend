from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from models import study as models
from schemas import study as schemas
from datetime import datetime, timedelta
from typing import List

def get_studies(db: Session, subject: str = None, study_type: str = None, completed: bool = None):
    query = db.query(models.Study)
    
    if subject:
        query = query.filter(models.Study.subject == subject)
    if study_type:
        query = query.filter(models.Study.study_type == study_type)
    if completed is not None:
        query = query.filter(models.Study.completed == completed)
    
    return query.order_by(desc(models.Study.created_at)).all()

def get_study(db: Session, study_id: int):
    return db.query(models.Study).filter(models.Study.id == study_id).first()

def create_study(db: Session, study: schemas.StudyCreate):
    db_study = models.Study(**study.model_dump())
    db.add(db_study)
    db.commit()
    db.refresh(db_study)
    return db_study

def update_study(db: Session, study_id: int, study_update: schemas.StudyUpdate):
    db_study = db.query(models.Study).filter(models.Study.id == study_id).first()
    if not db_study:
        return None
    
    update_data = study_update.model_dump(exclude_unset=True)
    
    # 進捗率を自動計算
    if 'completed_hours' in update_data and 'estimated_hours' in update_data:
        progress = min(100, int((update_data['completed_hours'] / update_data['estimated_hours']) * 100))
        update_data['progress_percentage'] = progress
    elif 'completed_hours' in update_data:
        progress = min(100, int((update_data['completed_hours'] / db_study.estimated_hours) * 100))
        update_data['progress_percentage'] = progress
    
    # 完了時の処理
    if 'completed' in update_data and update_data['completed']:
        update_data['completed_at'] = datetime.now()
        update_data['progress_percentage'] = 100
    elif 'completed' in update_data and not update_data['completed']:
        update_data['completed_at'] = None
    
    for key, value in update_data.items():
        setattr(db_study, key, value)
    
    db.commit()
    db.refresh(db_study)
    return db_study

def delete_study(db: Session, study_id: int):
    db_study = db.query(models.Study).filter(models.Study.id == study_id).first()
    if db_study:
        db.delete(db_study)
        db.commit()
        return True
    return False

def get_study_recommendations(db: Session, limit: int = 5):
    """おすすめの勉強タスクを取得"""
    # 未完了のタスクを取得
    incomplete_studies = db.query(models.Study).filter(models.Study.completed == False).all()
    
    recommendations = []
    for study in incomplete_studies:
        score = calculate_recommendation_score(study)
        reason = get_recommendation_reason(study, score)
        
        recommendations.append(schemas.StudyRecommendation(
            study=study,
            recommendation_score=score,
            reason=reason
        ))
    
    # スコア順にソート
    recommendations.sort(key=lambda x: x.recommendation_score, reverse=True)
    return recommendations[:limit]

def calculate_recommendation_score(study):
    """おすすめスコアを計算"""
    score = 0
    
    # 優先度によるスコア
    score += study.priority * 20
    
    # 期限によるスコア（期限が近いほど高スコア）
    if study.deadline:
        days_until_deadline = (study.deadline - datetime.now()).days
        if days_until_deadline <= 0:
            score += 50  # 期限切れ
        elif days_until_deadline <= 3:
            score += 40  # 3日以内
        elif days_until_deadline <= 7:
            score += 30  # 1週間以内
        elif days_until_deadline <= 14:
            score += 20  # 2週間以内
        else:
            score += 10  # それ以外
    
    # 進捗によるスコア（進捗が少ないほど高スコア）
    if study.progress_percentage < 25:
        score += 15
    elif study.progress_percentage < 50:
        score += 10
    elif study.progress_percentage < 75:
        score += 5
    
    # 難易度によるスコア（難易度が高いほど高スコア）
    score += study.difficulty * 5
    
    return score

def get_recommendation_reason(study, score):
    """おすすめ理由を生成"""
    reasons = []
    
    if study.priority >= 4:
        reasons.append("高優先度")
    
    if study.deadline:
        days_until_deadline = (study.deadline - datetime.now()).days
        if days_until_deadline <= 0:
            reasons.append("期限切れ")
        elif days_until_deadline <= 3:
            reasons.append("期限が迫っている")
    
    if study.progress_percentage < 25:
        reasons.append("進捗が少ない")
    
    if study.difficulty >= 4:
        reasons.append("高難易度")
    
    if not reasons:
        reasons.append("継続学習")
    
    return "、".join(reasons)

def get_study_history(db: Session, days: int = 30):
    """勉強履歴を取得"""
    start_date = datetime.now() - timedelta(days=days)
    return db.query(models.Study).filter(
        and_(
            models.Study.completed == True,
            models.Study.completed_at >= start_date
        )
    ).order_by(desc(models.Study.completed_at)).all()

def get_study_statistics(db: Session):
    """勉強統計を取得"""
    total_studies = db.query(models.Study).count()
    completed_studies = db.query(models.Study).filter(models.Study.completed == True).count()
    total_hours = db.query(func.sum(models.Study.completed_hours)).scalar() or 0
    
    # 科目別統計
    subject_stats = {}
    for subject in models.StudySubject:
        count = db.query(models.Study).filter(models.Study.subject == subject).count()
        completed = db.query(models.Study).filter(
            and_(models.Study.subject == subject, models.Study.completed == True)
        ).count()
        hours = db.query(func.sum(models.Study.completed_hours)).filter(
            models.Study.subject == subject
        ).scalar() or 0
        
        subject_stats[subject.value] = {
            "total": count,
            "completed": completed,
            "hours": hours
        }
    
    return {
        "total_studies": total_studies,
        "completed_studies": completed_studies,
        "completion_rate": (completed_studies / total_studies * 100) if total_studies > 0 else 0,
        "total_hours": total_hours,
        "subject_stats": subject_stats
    }

# 時間割関連
def get_timetable(db: Session, day_of_week: int = None):
    query = db.query(models.Timetable)
    if day_of_week is not None:
        query = query.filter(models.Timetable.day_of_week == day_of_week)
    return query.order_by(models.Timetable.start_time).all()

def create_timetable_entry(db: Session, timetable: schemas.TimetableCreate):
    db_timetable = models.Timetable(**timetable.model_dump())
    db.add(db_timetable)
    db.commit()
    db.refresh(db_timetable)
    return db_timetable

def update_timetable_entry(db: Session, timetable_id: int, timetable_update: schemas.TimetableUpdate):
    db_timetable = db.query(models.Timetable).filter(models.Timetable.id == timetable_id).first()
    if not db_timetable:
        return None
    
    update_data = timetable_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_timetable, key, value)
    
    db.commit()
    db.refresh(db_timetable)
    return db_timetable

def delete_timetable_entry(db: Session, timetable_id: int):
    db_timetable = db.query(models.Timetable).filter(models.Timetable.id == timetable_id).first()
    if db_timetable:
        db.delete(db_timetable)
        db.commit()
        return True
    return False

