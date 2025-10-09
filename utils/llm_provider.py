import os
from config.settings import settings
from langchain_groq import ChatGroq
# from langchain_google_genai import ChatGoogleGenerativeAI
from utils.logger import get_logger

logger = get_logger(name="llm_provider")

# Uncomment if using Gemini
# def get_llm():
#     logger.info("Initializing Gemini LLM (gemini-pro)")
#     return ChatGoogleGenerativeAI(
#         model="gemini-pro",
#         google_api_key=settings.GOOGLE_API_KEY,
#         temperature=0.1,
#         max_output_tokens=512,
#     )

def get_llm():
    logger.info("Initializing Groq LLM (llama3-70b-8192)")
    try:
        llm = ChatGroq(
            groq_api_key=settings.GROQ_API_KEY,
            model_name="llama3-70b-8192",
            temperature=0.01,
            max_tokens=512
        )
        logger.info("Groq LLM initialized successfully.")
        return llm
    except Exception as e:
        logger.exception(f"Failed to initialize Groq LLM: {e}")
        raise
