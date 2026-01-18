from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # APP
    APP_NAME: str = "Email Classifier API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # SERVIÇO (front no Live Server)
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ]

    # ML / AI
    MODEL_NAME: str = "tfidf-logreg"
    MODEL_VERSION: str = "v1"

    # API
    API_PREFIX: str = ""


settings = Settings()
