from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import settings

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.GOOGLE_API_KEY
    )
