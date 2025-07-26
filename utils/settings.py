from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import settings

from pydantic import BaseSettings

class Settings(BaseSettings):
    GOOGLE_API_KEY: str

settings = Settings()
