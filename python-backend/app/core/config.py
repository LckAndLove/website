# app/core/config.py
from pydantic import BaseModel
from starlette.config import Config

# 如果存在 .env 文件，从中加载环境变量
config = Config(".env")

class MailSettings(BaseModel):
    MAIL_USERNAME: str = config("MAIL_USERNAME", default="your-email@example.com")
    MAIL_PASSWORD: str = config("MAIL_PASSWORD", default="your-app-password")
    MAIL_FROM: str = config("MAIL_FROM", default="your-email@example.com")
    MAIL_PORT: int = config("MAIL_PORT", default=465)
    MAIL_SERVER: str = config("MAIL_SERVER", default="smtp.example.com")
    MAIL_FROM_NAME: str = config("MAIL_FROM_NAME", default="YourApp")
    MAIL_STARTTLS: bool = config("MAIL_STARTTLS", default=False)
    MAIL_SSL_TLS: bool = config("MAIL_SSL_TLS", default=True)
    USE_CREDENTIALS: bool = config("USE_CREDENTIALS", default=True)
    VALIDATE_CERTS: bool = config("VALIDATE_CERTS", default=True)

mail_settings = MailSettings()