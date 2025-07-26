# Placeholder for settings.py
# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    LMS_API_BASE_URL = os.getenv("LMS_API_BASE_URL")

settings = Settings()
