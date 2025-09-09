from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from models import coins as models
from schemas import coins as schemas
from crud import coins as crud

router = APIRouter(prefix="/coins", tags=["coins"])

# コイン取引関連
@router.get("/", response_model=List[schemas.Coin])
def read_coins(
    coin_type: Optional[str] = Query(None, description="コインタイプでフィルタ"),
    category: Optional[str] = Query(None, description="カテゴリでフィルタ"),
    limit: int = Query(100, description="取得件数"),
    db: Session = Depends(get_db)
):
    return crud.get_coins(db, coin_type, category, limit)

@router.get("/{coin_id}", response_model=schemas.Coin)
def read_coin(coin_id: int, db: Session = Depends(get_db)):
    coin = crud.get_coin(db, coin_id)
    if coin is None:
        raise HTTPException(status_code=404, detail="Coin not found")
    return coin

@router.post("/", response_model=schemas.Coin)
def create_coin(coin: schemas.CoinCreate, db: Session = Depends(get_db)):
    return crud.create_coin(db, coin)

@router.put("/{coin_id}", response_model=schemas.Coin)
def update_coin(coin_id: int, coin: schemas.CoinUpdate, db: Session = Depends(get_db)):
    db_coin = crud.update_coin(db, coin_id, coin)
    if db_coin is None:
        raise HTTPException(status_code=404, detail="Coin not found")
    return db_coin

@router.delete("/{coin_id}")
def delete_coin(coin_id: int, db: Session = Depends(get_db)):
    success = crud.delete_coin(db, coin_id)
    if not success:
        raise HTTPException(status_code=404, detail="Coin not found")
    return {"detail": "Coin deleted"}

@router.get("/balance/")
def get_current_balance(db: Session = Depends(get_db)):
    return {"balance": crud.get_current_balance(db)}

# コイン目標関連
@router.get("/goals/", response_model=List[schemas.CoinGoal])
def read_coin_goals(
    completed: Optional[bool] = Query(None, description="完了状態でフィルタ"),
    db: Session = Depends(get_db)
):
    return crud.get_coin_goals(db, completed)

@router.get("/goals/{goal_id}", response_model=schemas.CoinGoal)
def read_coin_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = crud.get_coin_goal(db, goal_id)
    if goal is None:
        raise HTTPException(status_code=404, detail="Coin goal not found")
    return goal

@router.post("/goals/", response_model=schemas.CoinGoal)
def create_coin_goal(goal: schemas.CoinGoalCreate, db: Session = Depends(get_db)):
    return crud.create_coin_goal(db, goal)

@router.put("/goals/{goal_id}", response_model=schemas.CoinGoal)
def update_coin_goal(goal_id: int, goal: schemas.CoinGoalUpdate, db: Session = Depends(get_db)):
    db_goal = crud.update_coin_goal(db, goal_id, goal)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Coin goal not found")
    return db_goal

@router.delete("/goals/{goal_id}")
def delete_coin_goal(goal_id: int, db: Session = Depends(get_db)):
    success = crud.delete_coin_goal(db, goal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Coin goal not found")
    return {"detail": "Coin goal deleted"}

# コインショップ関連
@router.get("/shop/", response_model=List[schemas.CoinShop])
def read_coin_shop_items(
    is_available: Optional[bool] = Query(None, description="利用可能状態でフィルタ"),
    db: Session = Depends(get_db)
):
    return crud.get_coin_shop_items(db, is_available)

@router.get("/shop/{item_id}", response_model=schemas.CoinShop)
def read_coin_shop_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_coin_shop_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Shop item not found")
    return item

@router.post("/shop/", response_model=schemas.CoinShop)
def create_coin_shop_item(item: schemas.CoinShopCreate, db: Session = Depends(get_db)):
    return crud.create_coin_shop_item(db, item)

@router.put("/shop/{item_id}", response_model=schemas.CoinShop)
def update_coin_shop_item(item_id: int, item: schemas.CoinShopUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_coin_shop_item(db, item_id, item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Shop item not found")
    return db_item

@router.delete("/shop/{item_id}")
def delete_coin_shop_item(item_id: int, db: Session = Depends(get_db)):
    success = crud.delete_coin_shop_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Shop item not found")
    return {"detail": "Shop item deleted"}

@router.post("/shop/{item_id}/purchase")
def purchase_coin_shop_item(item_id: int, db: Session = Depends(get_db)):
    result = crud.purchase_coin_shop_item(db, item_id)
    if result is None:
        raise HTTPException(status_code=400, detail="Cannot purchase item")
    return {"detail": "Item purchased successfully", "coin_transaction": result}

# 通貨交換関連
@router.get("/exchanges/", response_model=List[schemas.CoinExchange])
def read_coin_exchanges(
    limit: int = Query(50, description="取得件数"),
    db: Session = Depends(get_db)
):
    return crud.get_coin_exchanges(db, limit)

@router.post("/exchanges/", response_model=schemas.CoinExchange)
def create_coin_exchange(exchange: schemas.CoinExchangeCreate, db: Session = Depends(get_db)):
    return crud.create_coin_exchange(db, exchange)

@router.post("/exchange-to-points/")
def exchange_coins_to_points(
    coin_amount: int = Query(..., description="交換するコイン数"),
    exchange_rate: float = Query(1.0, description="交換レート"),
    db: Session = Depends(get_db)
):
    result = crud.exchange_coins_to_points(db, coin_amount, exchange_rate)
    if result is None:
        raise HTTPException(status_code=400, detail="Cannot exchange coins")
    return {"detail": "Exchange successful", "result": result}

# 統計関連
@router.get("/statistics/")
def get_coin_statistics(
    days: int = Query(30, description="過去何日分の統計を取得するか"),
    db: Session = Depends(get_db)
):
    return crud.get_coin_statistics(db, days)
