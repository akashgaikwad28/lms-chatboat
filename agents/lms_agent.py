import logging
from chains.course_recommender import run_course_recommender_chain
from chains.faq_chain import run_faq_chain
from chains.course_lookup import run_course_lookup_chain
from chains.counseling_chain import run_counseling_chain
from chains.concept_explainer import run_concept_explainer_chain
from utils.llm_provider import get_llm
from utils.prompt_loader import load_prompt_template

PROMPT_DIR = "prompts"

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize LLM
llm = get_llm()

# Load prompt for intent classification
intent_prompt = load_prompt_template(f"{PROMPT_DIR}/intent_classifier_prompt.txt")


# 🔍 Intent Classifier
async def classify_intent(user_query: str) -> str:
    """Classify the user query into one of the defined intents."""
    try:
        chain = intent_prompt | llm
        response = await chain.ainvoke({"query": user_query})
        intent = response.content.strip().lower()
        return intent
    except Exception as e:
        logger.error(f"Error during intent classification: {e}")
        return "other"


# 🤖 Agent Router
async def run_agent(user_query: str, user_id: str = None) -> str:
    """Route user query based on classified intent to the appropriate handler."""
    intent = await classify_intent(user_query)
    logger.info(f"Classified Intent: {intent} | Query: {user_query}")

    try:
        if intent == "recommendation":
            response = await run_course_recommender_chain(user_query, user_id)
            logger.info(f"Recommendation Response: {response}")
            return response

        elif intent == "faq":
            response = await run_faq_chain(user_query)
            logger.info(f"FAQ Response: {response}")
            return response

        elif intent == "course_lookup":
            response = await run_course_lookup_chain(user_query)
            logger.info(f"Course Lookup Response: {response}")
            return response

        elif intent == "counseling":
            response = await run_counseling_chain(user_query, user_id)
            logger.info(f"Counseling Response: {response}")
            return response

        elif intent == "concept_explanation":
            response = await run_concept_explainer_chain(user_query)
            logger.info(f"Concept Explanation Response: {response}")
            return response

        else:
            logger.warning(f"Unknown Intent: {intent} | Query: {user_query}")
            return (
                "🤖 I'm not sure how to help with that specific question.\n"
                "You can ask me things like:\n"
                "• What course should I take to learn AI?\n"
                "• Do you have Python or ML courses?\n"
                "• Can you help me choose a course based on my background?\n"
                "• What are the prices of your courses?\n"
            )

    except Exception as e:
        logger.error(f"Error in run_agent handler: {e}")
        return (
            "⚠️ Sorry, something went wrong while processing your request.\n"
            "Please try again later or contact support."
        )
