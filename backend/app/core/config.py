import secrets
import warnings
from pydantic import EmailStr
from pydantic import (AnyUrl, BeforeValidator, 
                      computed_field, model_validator, 
                      HttpUrl, PostgresDsn)
from typing import Annotated, Literal, Self
from pydantic_settings import BaseSettings, SettingsConfigDict



def parse_cors(v: str) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("[]"):
        return [i.strip() for i in v.split(",") if i.strip()]
    if isinstance(v, list | str):
        return v
    else:
        raise ValueError


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore"
    )

    PROJECT_NAME: str = 'Layterms'
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["local", "development", "production"] = "local"
    BACKEND_CORS_ORIGIN: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)]
    FRONTEND_HOST: str = "http://localhost:5173"
    SENTRY_DSN: HttpUrl | None = None
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE: int = 60 * 60 * 24 * 8
    RESET_TOKEN_EXPIRE: int = 60 * 15


    @computed_field
    @property
    def all_cors_origin(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGIN] + [
            self.FRONTEND_HOST]


    DATABASE_PORT: int = 5432
    DATABASE_SERVER: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str = ""
    DATABASE_NAME: str = ""

    @property
    @computed_field
    def DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            host=self.DATABASE_SERVER,
            username=self.DATABASE_USERNAME,
            password=self.DATABASE_PASSWORD,
            port=self.DATABASE_PORT,
            path=self.DATABASE_NAME
        )


    SMTP_SSL: bool = True
    SMTP_TLS: bool = False
    SMTP_HOST: str | None = None
    SMTP_PORT: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAIL_FROM_EMAIL: EmailStr | None = None
    EMAIL_FROM_NAME: str | None = None


    @model_validator(mode="after")
    def _set_default_email(self) -> Self:
        if not self.EMAIL_FROM_NAME:
            self.EMAIL_FROM_NAME = self.PROJECT_NAME
        return self

    @computed_field
    @property
    def enable_email(self) -> bool:
        return (self.SMTP_HOST, self.EMAIL_FROM_EMAIL)


settings = Settings()

