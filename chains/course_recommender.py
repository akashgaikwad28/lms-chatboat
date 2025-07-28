
# chains/course_recommender.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.lms_api_tool import get_available_courses
from config.settings import Settings
from utils.llm_provider import get_llm
import os

# Load Gemini LLM


llm = get_llm()

# Prompt template for course recommendation
recommend_prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant at an online learning platform.

Based on the student's interests and background described below, suggest 3 relevant courses. Be short and clear.

Student query: "{user_query}"

Here are the available courses:
{course_data}

Your response:
- List only 3 best-fit courses with name and short reason why each fits.
- Format it clearly.
""")

async def run_course_recommender_chain(user_query: str, user_id: str = None) -> str:
    try:
        # Get real-time courses from LMS API
        course_data = await get_available_courses()

        # If LMS fails, fallback to dummy data
        if not course_data:
            course_data = [
                {"title": "Python for Beginners", "category": "Programming", "level": "Beginner"},
                {"title": "ReactJS Web Development", "category": "Web Dev", "level": "Intermediate"},
                {"title": "AI Fundamentals", "category": "AI", "level": "Beginner"},
            ]

        # Convert to readable string for LLM
        course_text = "\n".join([
            f"- {course['title']} | {course.get('category', '')} | {course.get('level', '')}"
            for course in course_data
        ])

        chain = recommend_prompt | llm
        response = await chain.ainvoke({
            "user_query": user_query,
            "course_data": course_text
        })

        return response.content.strip()

    except Exception as e:
        print("Error in course recommender:", e)
        return "⚠️ Sorry, I'm unable to recommend courses at the moment. Please try again later."
