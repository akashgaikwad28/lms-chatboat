from utils.course_data_loader import load_course_data
from langchain_core.prompts import ChatPromptTemplate
from utils.llm_provider import get_llm
from utils.logger import get_logger
import traceback

logger = get_logger(name="course_lookup_chain")
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
        courses = load_course_data()

        if not courses:
            logger.warning("Course data is empty or failed to load.")
            return "⚠️ Sorry, I couldn't retrieve course information at the moment."

        available_courses = "\n".join([
            f"- {course['title']} | {course.get('category', '')} | ₹{course.get('pricing', 'N/A')}"
            for course in courses
        ])

        chain = course_lookup_prompt | llm
        response = await chain.ainvoke({
            "user_query": user_query,
            "available_courses": available_courses
        })

        logger.info("[Course Lookup] Response generated successfully.")
        return response.content.strip()

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)[-1]
        logger.error(
            f"\n--- Exception in run_course_lookup_chain ---\n"
            f"File      : {tb.filename}\n"
            f"Function  : {tb.name}\n"
            f"Line No   : {tb.lineno}\n"
            f"Error     : {type(e).__name__} - {str(e)}\n"
            f"---------------------------------------------"
        )
        logger.debug("Full Traceback:\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__)))
        return "⚠️ Sorry, I couldn't retrieve course information at the moment."
