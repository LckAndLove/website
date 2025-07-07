# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"  # 使用 SQLite 数据库，文件名为 test.db

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} # check_same_thread 是 SQLite 特有的配置
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)