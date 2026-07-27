import secrets
import warnings
from pydantic import (AnyUrl, BeforeValidator, 
                      computed_field, model_validator, 
                      HttpUrl)
from typing import Annotated
from typing import Literal
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


    @computed_field
    @property
    def all_cors_origin(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGIN] + [
            self.FRONTEND_HOST]

settings = Settings()

