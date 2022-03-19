import os

from pydantic import BaseSettings, validator


class MLSettings(BaseSettings):
    max_iterations: int = os.getenv("MAX_ITERATIONS")


class Settings(BaseSettings):
    ml: MLSettings = MLSettings()
    api_prefix: str = os.getenv("APP_API_PREFIX")
    celery_result_ttl: int = os.getenv("CELERY_RESULT_TTL")

    @validator("api_prefix", pre=True)
    def is_valid_api_prefix(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError(
                f"API prefix should have str type, got {type(value)} instead"
            )
        return value


settings = Settings()
