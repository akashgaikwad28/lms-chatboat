# chains/faq_chain.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.llm_provider import get_llm
from config.settings import settings
import os

# Load Gemini model


llm = get_llm()



# Prompt template for FAQ answering
faq_prompt = ChatPromptTemplate.from_template("""
You are a support assistant for **Acash Tech**, an online LMS platform. Answer user questions clearly and in a friendly tone.

Only respond based on facts about Acash Tech or general LMS behavior.

Answer the student's question clearly and politely using the following FAQs as your reference:

FAQs:
1. How do I enroll in a course? → You can log in, go to the courses page, and click “Enroll” or “Buy Now”.
2. What payment methods are supported? → We support PayPal and credit/debit cards.
3. Can I track my course progress? → Yes, go to "My Courses" and see your progress.
4. What if I forget my password? → Click "Forgot password" on the login page.
5. Can I contact the course instructor? → Yes, each course page has a contact form.
6. How do I reset my course progress? → Go to "My Courses" → "Settings" → "Reset Progress".
7. Can I get a refund? → Yes, within 7 days of purchase if less than 30% of course completed.

Student Question: "{user_question}"

Give a helpful, student-friendly response.
""")

async def run_faq_chain(user_question: str) -> str:
    try:
        chain = faq_prompt | llm
        response = await chain.ainvoke({
            "user_question": user_question
        })

        return response.content.strip()
    except Exception as e:
        print("FAQ Chain Error:", e)
        return "⚠️ Sorry, I'm having trouble answering that right now. Please try again later."
