from dotenv import load_dotenv
import os
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from typing import List

load_dotenv()


class Settings(BaseSettings):
    # base
    WORKERS: int = 1
    VERSION: str = os.getenv("1.0.0", "VERSION")
    HOST: str = "localhost"
    PREFIX: str = "/api"
    PORT: int = 8080
    RELOAD: bool = False
    CORS_ORIGINS: List[AnyHttpUrl] = []
    CORS_ORIGIN_REGEX: str | None = None
    # database
    DATABASE_URL: str = os.getenv("", "DATABASE_URL")
    ECHO: bool = False
    ECHO_POOL: bool = False
    POOL_SIZE: int = 50
    MAX_OVERFLOW: int = 10
    NAMING_CONVENTION: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    CELERY_TIMEZONE: str = os.getenv("CELERY_TIMEZONE", "")
    # Static
    STATIC_DIR: str = os.getenv("STATIC_DIR", "./api/static/")
    # email
    SMTP_HOST: str = os.getenv("", "EMAIL_HOST")
    SMTP_USERNAME: str = os.getenv("", "EMAIL_USERNAME")
    SMTP_PASSWORD: str = os.getenv("", "EMAIL_PASSWORD")
    SMTP_PORT: str = os.getenv("", "EMAIL_PORT")
    SMTP_SENDER: str = os.getenv("", "SMTP_SENDER")

    # Expo push notifications
    EXPO_NOTIFICATIONS_URL: str = os.getenv("", "EXPO_NOTIFICATIONS_URL")
    # RabbitMQ
    RABBIT_USER: str = os.getenv("", "RABBIT_USER")
    RABBIT_PASSWORD: str = os.getenv("", "RABBIT_PASSWORD")


class LocalSettings(Settings):
    RELOAD: bool = True


class DevSettings(Settings):
    WORKERS: int = 4
    CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:5173",
        "http://localhost:8081",
        "http://музеум.рф",
        "http://xn--e1adoc6ac.xn--p1ai",
        "http://80.87.111.240",
        "http://91.229.234.70"
    ]
    CORS_ORIGIN_REGEX: str = (
        r"(http:\/\/80\.87\.111\.240|http:\/\/91\.229\.234\.70|http:\/\/музеум\.рф|http:\/\/xn--e1adoc6ac\.xn--p1ai|http:\/\/localhost:5173|http:\/\/localhost:8081)"
    )


settings_by_name = {
    "dev": DevSettings,
    "local": LocalSettings,
}

settings = settings_by_name[os.getenv("API_MODE") or "local"]()
