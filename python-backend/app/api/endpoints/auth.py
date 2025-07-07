# app/api/endpoints/auth.py (最终版，从环境变量加载配置)
import random
import time
import smtplib
from datetime import timedelta
from email.message import EmailMessage

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.crud import user as crud_user
from app.schemas.user import UserCreate, UserInDB, Token, EmailSchema
from app.core import security
from app.db.session import SessionLocal
from app.core.config import mail_settings # ❗️ 导入配置实例

router = APIRouter()
verification_codes = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 这个函数现在直接使用导入的 mail_settings
def send_verification_email_sync(email_to: str, code: str):
    msg = EmailMessage()
    msg['Subject'] = "您的注册验证码"
    msg['From'] = f"{mail_settings.MAIL_FROM_NAME} <{mail_settings.MAIL_USERNAME}>"
    msg['To'] = email_to
    msg.set_content(f"欢迎注册！您的验证码是：{code}，有效期为5分钟。")

    try:
        server = smtplib.SMTP(mail_settings.MAIL_SERVER, mail_settings.MAIL_PORT, timeout=20)
        server.starttls()
        server.login(mail_settings.MAIL_USERNAME, mail_settings.MAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ Verification email sent to {email_to}")
    except Exception as e:
        print(f"❌ Failed to send email to {email_to}: {e}")

@router.post("/request-code", summary="请求邮箱验证码")
async def request_verification_code(
    email_schema: EmailSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    if crud_user.get_user_by_email(db, email=email_schema.email):
        raise HTTPException(status_code=400, detail="此邮箱已被注册")

    code = f"{random.randint(0, 999999):06d}"
    verification_codes[email_schema.email] = {"code": code, "timestamp": time.time()}
    
    background_tasks.add_task(send_verification_email_sync, email_schema.email, code)
    
    return {"message": "验证码发送请求已提交，请检查您的邮箱"}

# /register 和 /login 接口保持不变
@router.post("/register", response_model=UserInDB, summary="使用邮箱和验证码注册")
def register(user: UserCreate, db: Session = Depends(get_db)):
    stored_data = verification_codes.get(user.email)
    if not stored_data:
        raise HTTPException(status_code=400, detail="请先请求验证码")
    if time.time() - stored_data["timestamp"] > 300:
        raise HTTPException(status_code=400, detail="验证码已过期")
    if stored_data["code"] != user.code:
        raise HTTPException(status_code=400, detail="验证码错误")

    if crud_user.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="此邮箱已被注册")

    db_user = crud_user.create_user(db=db, user=user)
    del verification_codes[user.email]
    return db_user

@router.post("/login", response_model=Token, summary="登录")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码不正确",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}