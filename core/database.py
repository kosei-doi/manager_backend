from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"  # データベースファイルパス
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ここがポイント
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# from core.database import Base, engine
# from models import tasks  # tasks.py をimport

# # 既存のテーブルを削除
# Base.metadata.drop_all(bind=engine)
# # モデルに基づいてテーブルを作り直す
# Base.metadata.create_all(bind=engine)

# print("DBをリセットしてモデルと同期しました")
