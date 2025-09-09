from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import tasks, reminders, schedules, study, meals, points, coins
from core.database import Base, engine
from models import tasks as models
from init_data import init_data

# データベーステーブルの作成
Base.metadata.create_all(bind=engine)

# 初期データの挿入
init_data()

app = FastAPI()

# CORS設定を追加
import os

# 本番環境と開発環境のオリジンを設定
allowed_origins = [
    "http://localhost:8080",  # Vue.jsの開発サーバー
    "http://localhost:8081",  # Vue.jsの開発サーバー（ポート8081）
    "http://localhost:8082",  # Vue.jsの開発サーバー（ポート8082）
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
    "http://127.0.0.1:8082"
]

# 本番環境のフロントエンドURLが設定されている場合は追加
if os.getenv("FRONTEND_URL"):
    allowed_origins.append(os.getenv("FRONTEND_URL"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)
app.include_router(reminders.router)
app.include_router(schedules.router)
app.include_router(study.router)
app.include_router(meals.router)
app.include_router(points.router)
app.include_router(coins.router)
