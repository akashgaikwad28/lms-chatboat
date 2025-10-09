from chains.course_recommender import run_course_recommender_chain
from chains.faq_chain import run_faq_chain
from chains.course_lookup import run_course_lookup_chain
from chains.counseling_chain import run_counseling_chain
from chains.concept_explainer import run_concept_explainer_chain
from utils.llm_provider import get_llm
from utils.prompt_loader import load_prompt_template
from utils.logger import get_logger
import traceback

PROMPT_DIR = "prompts"
logger = get_logger(name="lms_agent")

llm = get_llm()
intent_prompt = load_prompt_template(f"{PROMPT_DIR}/intent_classifier_prompt.txt")

# Intent Classifier
async def classify_intent(user_query: str) -> str:
    try:
        logger.info(f"[Intent Classification] Query: {user_query}")
        chain = intent_prompt | llm
        response = await chain.ainvoke({"query": user_query})
        intent = response.content.strip().lower()
        logger.info(f"[Intent Classification] Classified as: {intent}")
        return intent
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)[-1]
        logger.error(
            f"\n--- Exception in classify_intent ---\n"
            f"File      : {tb.filename}\n"
            f"Function  : {tb.name}\n"
            f"Line No   : {tb.lineno}\n"
            f"Error     : {type(e).__name__} - {str(e)}\n"
            f"-------------------------------------"
        )
        logger.debug("Full Traceback:\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__)))
        return "other"

# Agent Dispatcher
async def run_agent(user_query: str, user_id: str = None, user_name: str = None) -> str:
    intent = await classify_intent(user_query)
    logger.info(f"[Agent Router] Intent: {intent} | Query: {user_query}")

    try:
        if intent == "recommendation":
            response = await run_course_recommender_chain(user_query, user_id)
            logger.info(f"[Agent Router] Recommendation Response: {response}")
            return response

        elif intent == "faq":
            response = await run_faq_chain(user_query)
            logger.info(f"[Agent Router] FAQ Response: {response}")
            return response

        elif intent == "course_lookup":
            response = await run_course_lookup_chain(user_query)
            logger.info(f"[Agent Router] Course Lookup Response: {response}")
            return response

        elif intent == "counseling":
            response = await run_counseling_chain(user_query, user_id)
            logger.info(f"[Agent Router] Counseling Response: {response}")
            return response

        elif intent == "concept_explanation":
            response = await run_concept_explainer_chain(user_query)
            logger.info(f"[Agent Router] Concept Explanation Response: {response}")
            return response

        elif intent == "greeting":
            logger.info("[Agent Router] Greeting intent detected.")
            return (
                "👋 Hello Learner! I'm your Acash Tech Assistant.\n"
                "I can help you with course recommendations, pricing, and more.\n"
                "Try asking something like:\n"
                "• What courses are available for Python?\n"
                "• Can you help me choose a course?\n"
                "• What's the price of the AI course?\n"
            )

        else:
            logger.warning(f"[Agent Router] Unknown Intent: {intent} | Query: {user_query}")
            return (
                "🤖 I'm not sure how to help with that specific question.\n"
                "You can ask me things like:\n"
                "• What course should I take to learn AI?\n"
                "• Do you have Python or ML courses?\n"
                "• Can you help me choose a course based on my background?\n"
                "• What are the prices of your courses?\n"
            )

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)[-1]
        logger.error(
            f"\n--- Exception in run_agent ---\n"
            f"File      : {tb.filename}\n"
            f"Function  : {tb.name}\n"
            f"Line No   : {tb.lineno}\n"
            f"Error     : {type(e).__name__} - {str(e)}\n"
            f"--------------------------------"
        )
        logger.debug("Full Traceback:\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__)))
        return (
            "⚠️ Sorry, something went wrong while processing your request.\n"
            "Please try again later or contact support."
        )
