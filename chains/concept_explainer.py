from langchain_core.prompts import ChatPromptTemplate
from utils.llm_provider import get_llm
from utils.logger import get_logger
import traceback

logger = get_logger(name="concept_explainer")

llm = get_llm()

explain_prompt = ChatPromptTemplate.from_template("""
You are a knowledgeable and beginner-friendly assistant.

Please explain the following concept clearly, with examples if appropriate:

Concept: "{user_query}"

Explanation:
""")

async def run_concept_explainer_chain(user_query: str) -> str:
    try:
        logger.info(f"[Concept Explanation] Query: {user_query}")
        chain = explain_prompt | llm
        response = await chain.ainvoke({"user_query": user_query})
        logger.info(f"[Concept Explanation] Response generated successfully.")
        return response.content.strip()

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)[-1]
        logger.error(
            f"\n--- Exception in run_concept_explainer_chain ---\n"
            f"File      : {tb.filename}\n"
            f"Function  : {tb.name}\n"
            f"Line No   : {tb.lineno}\n"
            f"Error     : {type(e).__name__} - {str(e)}\n"
            f"-----------------------------------------------"
        )
        logger.debug("Full Traceback:\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__)))
        return "⚠️ Sorry, I couldn't explain that concept right now. Try again later."
