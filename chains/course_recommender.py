from langchain_core.prompts import ChatPromptTemplate
from utils.llm_provider import get_llm
from utils.course_data_loader import load_course_data
from utils.logger import get_logger
import traceback

logger = get_logger(name="course_recommender_chain")

# Load LLM
llm = get_llm()

# Load course recommendation prompt from external file
try:
    with open("prompts/course_recommendation_prompt.txt", "r", encoding="utf-8") as f:
        prompt_template_str = f.read()
    logger.info("✅ Loaded course recommendation prompt successfully.")
except Exception as e:
    tb = traceback.extract_tb(e.__traceback__)[-1]
    logger.error(
        f"\n--- Error loading prompt file ---\n"
        f"File      : {tb.filename}\n"
        f"Function  : {tb.name}\n"
        f"Line No   : {tb.lineno}\n"
        f"Error     : {type(e).__name__} - {str(e)}\n"
        f"----------------------------------"
    )
    logger.debug("Full Traceback:\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__)))
    raise

recommend_prompt = ChatPromptTemplate.from_template(prompt_template_str)

async def run_course_recommender_chain(user_query: str, user_id: str = None) -> str:
    try:
        logger.info(f"[Course Recommender] Query from user_id={user_id}: {user_query}")

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
        logger.info(f"[Formatted Courses] {len(course_data)} courses prepared for prompt.")

        # Step 3: Chain prompt + LLM
        chain = recommend_prompt | llm
        response = await chain.ainvoke({
            "user_query": user_query,
            "course_data": course_text
        })

        logger.info(f"[LLM Recommendation Response] Generated successfully.")
        return response.content.strip()

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)[-1]
        logger.error(
            f"\n--- Exception in run_course_recommender_chain ---\n"
            f"File      : {tb.filename}\n"
            f"Function  : {tb.name}\n"
            f"Line No   : {tb.lineno}\n"
            f"Error     : {type(e).__name__} - {str(e)}\n"
            f"-----------------------------------------------"
        )
        logger.debug("Full Traceback:\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__)))
        return "⚠️ Sorry, I'm unable to recommend courses at the moment. Please try again later."
