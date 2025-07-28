# config/settings.py
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    GOOGLE_API_KEY: str = Field(..., alias="GOOGLE_API_KEY")
    LMS_API_BASE_URL: str = Field(..., alias="LMS_API_BASE_URL")

    class Config:
        env_file = ".env"
        populate_by_name = True

settings = Settings()
