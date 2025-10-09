from utils.llm_provider import get_llm
from utils.prompt_loader import load_prompt_template
from utils.logger import get_logger
import traceback

logger = get_logger(name="faq_chain")
llm = get_llm()

PROMPT_PATH = "prompts/faq_prompt.txt"
faq_prompt = load_prompt_template(PROMPT_PATH)

async def run_faq_chain(user_question: str) -> str:
    try:
        logger.info(f"[FAQ Chain] Received question: {user_question}")
        chain = faq_prompt | llm
        response = await chain.ainvoke({
            "user_question": user_question
        })
        logger.info("[FAQ Chain] Response generated successfully.")
        return response.content.strip()

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)[-1]
        logger.error(
            f"\n--- Exception in run_faq_chain ---\n"
            f"File      : {tb.filename}\n"
            f"Function  : {tb.name}\n"
            f"Line No   : {tb.lineno}\n"
            f"Error     : {type(e).__name__} - {str(e)}\n"
            f"-----------------------------------"
        )
        logger.debug("Full Traceback:\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__)))
        return "⚠️ Sorry, I'm having trouble answering that right now. Please try again later."
