# main.py
from fastapi import FastAPI
from app.api.endpoints import auth
from app.db.session import engine
from app.models import user

# 创建数据库表
user.Base.metadata.create_all(bind=engine)

app = FastAPI(title="My Python Backend")

# 包含认证路由
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Python Backend!"}