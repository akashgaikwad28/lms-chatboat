from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str
    GOOGLE_API_KEY: str = "" 

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
