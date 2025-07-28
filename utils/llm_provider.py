# utils/llm_provider.py

from langchain_google_genai import ChatGoogleGenerativeAI

from config.settings import settings


print("Using Google API key:", settings.GOOGLE_API_KEY)

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=settings.GOOGLE_API_KEY  
    )
