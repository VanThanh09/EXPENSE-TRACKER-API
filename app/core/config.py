from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    app_name: str = "BLOG-API"
    database_url: str
    secret_key: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8"
    )

settings = Settings()