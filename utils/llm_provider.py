# utils/llm_provider.py

from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import settings

def get_llm(model: str = "gemini-2.5-flash"):
    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=settings.GOOGLE_API_KEY
    )
