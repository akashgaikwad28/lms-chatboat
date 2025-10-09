from utils.llm_provider import get_llm
from utils.prompt_loader import load_prompt_template
from utils.course_data_loader import load_course_data
from utils.logger import get_logger
import traceback

PROMPT_PATH = "prompts/counseling_prompt.txt"
logger = get_logger(name="counseling_chain")

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

        logger.info(f"[Counseling] Response generated successfully for user_id={user_id}")
        return response.content.strip()

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)[-1]
        logger.error(
            f"\n--- Exception in run_counseling_chain ---\n"
            f"File      : {tb.filename}\n"
            f"Function  : {tb.name}\n"
            f"Line No   : {tb.lineno}\n"
            f"Error     : {type(e).__name__} - {str(e)}\n"
            f"------------------------------------------"
        )
        logger.debug("Full Traceback:\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__)))
        return "⚠️ I'm unable to provide counseling help right now. Please try again soon."
