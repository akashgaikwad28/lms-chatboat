from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    GEMINI_API_KEY: str = Field(..., alias="GEMINI API KEY")
    LMS_API_BASE_URL: str = Field(..., alias="LMS API BASE URL")

    class Config:
        env_file = ".env"
        populate_by_name = True



settings = Settings()