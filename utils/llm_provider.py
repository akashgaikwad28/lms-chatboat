# utils/llm_provider.py

from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import settings

print("Using Google API key:", settings.GEMINI_API_KEY)



def get_llm(model: str = "gemini-2.5-flash"):
    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=settings.GEMINI_API_KEY  # ✅ corrected here
    )
