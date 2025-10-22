from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./data.db"  # Cambia a tu Postgres más tarde
    API_TITLE: str = "Inventory API"
    API_VERSION: str = "0.1.0"
    class Config:
        env_file = ".env"

settings = Settings()
