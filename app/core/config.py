from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "makan Backend"
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
