# chains/course_lookup.py

import logging
from utils.course_data_loader import load_course_data
from langchain_core.prompts import ChatPromptTemplate
from utils.llm_provider import get_llm

logger = logging.getLogger(__name__)
llm = get_llm()

course_lookup_prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant at an online learning platform.

User query: {user_query}

Here are some available courses:
{available_courses}

Instructions:
- If a relevant course is found, return its name and price.
- If not, say: "❌ No matching course found."
- Be concise and helpful.
""")

async def run_course_lookup_chain(user_query: str) -> str:
    try:
        logger.info(f"[Course Lookup] Query: {user_query}")
        courses =  load_course_data()

        if not courses:
            return "⚠️ Sorry, I couldn't retrieve course information at the moment."

        # Format courses into plain string (NOT Jinja expressions)
        available_courses = "\n".join([
            f"- {course['title']} | {course.get('category', '')} | ₹{course.get('pricing', 'N/A')}"
            for course in courses
        ])

        chain = course_lookup_prompt | llm
        response = await chain.ainvoke({
            "user_query": user_query,
            "available_courses": available_courses
        })

        return response.content.strip()

    except Exception as e:
        logger.error(f"Error in course lookup chain: {e}", exc_info=True)
        return "⚠️ Sorry, I couldn't retrieve course information at the moment."
