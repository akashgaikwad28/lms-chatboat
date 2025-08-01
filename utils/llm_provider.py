# utils/llm_provider.py

# from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_groq import ChatGroq

from config.settings import settings


# print("Using Google API key:", settings.GOOGLE_API_KEY)

# def get_llm():
#     return ChatGoogleGenerativeAI(
#         model="gemini-pro",
#         google_api_key=settings.GOOGLE_API_KEY,
#         temperature=0.1,
#         max_output_tokens=512,
#     )



def get_llm():
    return ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model_name="llama3-70b-8192" ,
        temperature=0.01,
        max_tokens=512  
    )