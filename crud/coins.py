from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from datetime import datetime, timedelta
from typing import List
from models import coins as models
from schemas import coins as schemas

def get_coins(db: Session, coin_type: str = None, category: str = None, limit: int = 100):
    query = db.query(models.Coin)
    if coin_type:
        query = query.filter(models.Coin.coin_type == coin_type)
    if category:
        query = query.filter(models.Coin.category == category)
    return query.order_by(models.Coin.created_at.desc()).limit(limit).all()

def get_coin(db: Session, coin_id: int):
    return db.query(models.Coin).filter(models.Coin.id == coin_id).first()

def create_coin(db: Session, coin: schemas.CoinCreate):
    # 現在の残高を計算
    current_balance = get_current_balance(db)
    new_balance = current_balance + coin.amount if coin.coin_type == "earned" else current_balance - coin.amount
    
    db_coin = models.Coin(**coin.model_dump(), balance_after=new_balance)
    db.add(db_coin)
    db.commit()
    db.refresh(db_coin)
    return db_coin

def update_coin(db: Session, coin_id: int, coin: schemas.CoinUpdate):
    db_coin = db.query(models.Coin).filter(models.Coin.id == coin_id).first()
    if db_coin:
        update_data = coin.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_coin, field, value)
        db.commit()
        db.refresh(db_coin)
    return db_coin

def delete_coin(db: Session, coin_id: int):
    db_coin = db.query(models.Coin).filter(models.Coin.id == coin_id).first()
    if db_coin:
        db.delete(db_coin)
        db.commit()
        return True
    return False

def get_current_balance(db: Session):
    """現在のコイン残高を取得"""
    latest_coin = db.query(models.Coin).order_by(models.Coin.created_at.desc()).first()
    return latest_coin.balance_after if latest_coin else 0

def get_coin_goals(db: Session, completed: bool = None):
    query = db.query(models.CoinGoal)
    if completed is not None:
        query = query.filter(models.CoinGoal.completed == completed)
    return query.order_by(models.CoinGoal.created_at.desc()).all()

def get_coin_goal(db: Session, goal_id: int):
    return db.query(models.CoinGoal).filter(models.CoinGoal.id == goal_id).first()

def create_coin_goal(db: Session, goal: schemas.CoinGoalCreate):
    db_goal = models.CoinGoal(**goal.model_dump())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def update_coin_goal(db: Session, goal_id: int, goal: schemas.CoinGoalUpdate):
    db_goal = db.query(models.CoinGoal).filter(models.CoinGoal.id == goal_id).first()
    if db_goal:
        update_data = goal.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_goal, field, value)
        
        # 目標達成時の処理
        if update_data.get('completed') and not db_goal.completed:
            db_goal.completed_at = datetime.now()
        
        db.commit()
        db.refresh(db_goal)
    return db_goal

def delete_coin_goal(db: Session, goal_id: int):
    db_goal = db.query(models.CoinGoal).filter(models.CoinGoal.id == goal_id).first()
    if db_goal:
        db.delete(db_goal)
        db.commit()
        return True
    return False

def get_coin_shop_items(db: Session, is_available: bool = None):
    query = db.query(models.CoinShop)
    if is_available is not None:
        query = query.filter(models.CoinShop.is_available == is_available)
    return query.order_by(models.CoinShop.cost.asc()).all()

def get_coin_shop_item(db: Session, item_id: int):
    return db.query(models.CoinShop).filter(models.CoinShop.id == item_id).first()

def create_coin_shop_item(db: Session, item: schemas.CoinShopCreate):
    db_item = models.CoinShop(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_coin_shop_item(db: Session, item_id: int, item: schemas.CoinShopUpdate):
    db_item = db.query(models.CoinShop).filter(models.CoinShop.id == item_id).first()
    if db_item:
        update_data = item.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_coin_shop_item(db: Session, item_id: int):
    db_item = db.query(models.CoinShop).filter(models.CoinShop.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False

def purchase_coin_shop_item(db: Session, item_id: int):
    """ショップアイテムを購入"""
    db_item = db.query(models.CoinShop).filter(models.CoinShop.id == item_id).first()
    if not db_item or not db_item.is_available:
        return None
    
    # 在庫チェック
    if db_item.stock != -1 and db_item.stock <= 0:
        return None
    
    current_balance = get_current_balance(db)
    if current_balance < db_item.cost:
        return None
    
    # コインを消費
    coin_data = {
        "amount": db_item.cost,
        "coin_type": "spent",
        "category": "shopping",
        "description": f"ショップ購入: {db_item.title}",
        "balance_after": current_balance - db_item.cost
    }
    
    db_coin = models.Coin(**coin_data)
    db.add(db_coin)
    
    # アイテムの使用回数を更新
    db_item.used_count += 1
    if db_item.stock != -1:
        db_item.stock -= 1
        if db_item.stock <= 0:
            db_item.is_available = False
    
    db.commit()
    db.refresh(db_coin)
    return db_coin

def get_coin_exchanges(db: Session, limit: int = 50):
    """通貨交換履歴を取得"""
    return db.query(models.CoinExchange).order_by(models.CoinExchange.created_at.desc()).limit(limit).all()

def create_coin_exchange(db: Session, exchange: schemas.CoinExchangeCreate):
    db_exchange = models.CoinExchange(**exchange.model_dump())
    db.add(db_exchange)
    db.commit()
    db.refresh(db_exchange)
    return db_exchange

def exchange_coins_to_points(db: Session, coin_amount: int, exchange_rate: float = 1.0):
    """コインをポイントに交換"""
    current_balance = get_current_balance(db)
    if current_balance < coin_amount:
        return None
    
    point_amount = int(coin_amount * exchange_rate)
    
    # コインを消費
    coin_data = {
        "amount": coin_amount,
        "coin_type": "exchange",
        "category": "other",
        "description": f"ポイント交換: {coin_amount}コイン → {point_amount}ポイント",
        "balance_after": current_balance - coin_amount
    }
    
    db_coin = models.Coin(**coin_data)
    db.add(db_coin)
    
    # 交換履歴を記録
    exchange_data = {
        "from_currency": "coin",
        "to_currency": "point",
        "from_amount": coin_amount,
        "to_amount": point_amount,
        "exchange_rate": exchange_rate,
        "description": f"コイン→ポイント交換"
    }
    
    db_exchange = models.CoinExchange(**exchange_data)
    db.add(db_exchange)
    
    db.commit()
    db.refresh(db_coin)
    return {"coin_transaction": db_coin, "exchange_record": db_exchange, "point_amount": point_amount}

def get_coin_statistics(db: Session, days: int = 30):
    """コイン統計を取得"""
    start_date = datetime.now() - timedelta(days=days)
    
    # 期間中のコイン取引
    coins = db.query(models.Coin).filter(
        models.Coin.created_at >= start_date
    ).all()
    
    total_earned = sum(c.amount for c in coins if c.coin_type == "earned")
    total_spent = sum(c.amount for c in coins if c.coin_type == "spent")
    current_balance = get_current_balance(db)
    
    # 月間統計
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_coins = db.query(models.Coin).filter(
        models.Coin.created_at >= month_start
    ).all()
    
    monthly_earned = sum(c.amount for c in monthly_coins if c.coin_type == "earned")
    monthly_spent = sum(c.amount for c in monthly_coins if c.coin_type == "spent")
    
    # カテゴリ別統計
    category_stats = {}
    for coin in coins:
        if coin.coin_type == "earned":
            category_stats[coin.category] = category_stats.get(coin.category, 0) + coin.amount
    
    top_categories = [
        {"category": cat, "amount": amount}
        for cat, amount in sorted(category_stats.items(), key=lambda x: x[1], reverse=True)[:5]
    ]
    
    return {
        "total_earned": total_earned,
        "total_spent": total_spent,
        "current_balance": current_balance,
        "total_transactions": len(coins),
        "monthly_earned": monthly_earned,
        "monthly_spent": monthly_spent,
        "top_categories": top_categories
    }
