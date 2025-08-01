# chains/course_recommender.py

import logging
from langchain_core.prompts import ChatPromptTemplate
from utils.llm_provider import get_llm
from utils.course_data_loader import load_course_data

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load LLM
llm = get_llm()

# Load course recommendation prompt from external file
with open("prompts/course_recommendation_prompt.txt", "r", encoding="utf-8") as f:
    prompt_template_str = f.read()

# ChatPromptTemplate using loaded prompt
recommend_prompt = ChatPromptTemplate.from_template(prompt_template_str)

async def run_course_recommender_chain(user_query: str, user_id: str = None) -> str:
    try:
        logger.info(f"[User Query] {user_query}")

        # Step 1: Load course data from LMS API or fallback
        course_data = load_course_data()

        if not course_data:
            logger.warning("No course data found from LMS or fallback.")
            return "⚠️ No courses are available at the moment. Please check back later."

        # Step 2: Format course list into string for prompt
        course_text = "\n".join([
            f"- {course['title']} | {course.get('category', 'Unknown')} | {course.get('level', 'Unknown')}"
            for course in course_data
        ])
        logger.info(f"[Formatted Courses] {course_text}")

        # Step 3: Chain prompt + LLM
        chain = recommend_prompt | llm
        response = await chain.ainvoke({
            "user_query": user_query,
            "course_data": course_text
        })

        logger.info(f"[LLM Recommendation Response] {response.content}")
        return response.content.strip()

    except Exception as e:
        logger.error(f"Error in course recommender: {e}", exc_info=True)
        return "⚠️ Sorry, I'm unable to recommend courses at the moment. Please try again later."
