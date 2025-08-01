# chains/counseling_chain.py

import logging
from utils.llm_provider import get_llm
from utils.prompt_loader import load_prompt_template
from utils.course_data_loader import load_course_data

PROMPT_PATH = "prompts/counseling_prompt.txt"
logger = logging.getLogger(__name__)

llm = get_llm()
counseling_prompt = load_prompt_template(PROMPT_PATH)

async def run_counseling_chain(user_query: str, user_id: str = None) -> str:
    try:
        logger.info(f"[Counseling] Starting session for user_id={user_id} | Query: {user_query}")
        
        course_data = load_course_data()
        course_text = "\n".join([
            f"- {course['title']} | {course.get('category')} | {course.get('level')} | ₹{course.get('pricing')}"
            for course in course_data
        ])

        chain = counseling_prompt | llm
        response = await chain.ainvoke({
            "user_query": user_query,
            "course_catalog": course_text,
            "user_id": user_id or "anonymous"
        })

        return response.content.strip()

    except Exception as e:
        logger.error(f"Error in counseling chain: {e}")
        return "⚠️ I'm unable to provide counseling help right now. Please try again soon."
