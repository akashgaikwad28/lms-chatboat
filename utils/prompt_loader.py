import os
from langchain_core.prompts import ChatPromptTemplate
from utils.logger import get_logger
import traceback

logger = get_logger(name="prompt_loader")

def load_prompt_template(path: str) -> ChatPromptTemplate:
    """
    Load a prompt template from a given file path.

    Args:
        path (str): Path to the prompt template file.

    Returns:
        ChatPromptTemplate: LangChain-compatible prompt template.
    """
    try:
        logger.info(f"Loading prompt template from: {path}")

        if not os.path.exists(path):
            logger.error(f"Prompt file not found: {path}")
            raise FileNotFoundError(f"Prompt file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            template = f.read()

        logger.info(f"Successfully loaded prompt template from: {path}")
        return ChatPromptTemplate.from_template(template)

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)[-1]
        log_message = (
            f"\n--- Prompt Load Exception ---\n"
            f"File          : {tb.filename}\n"
            f"Function      : {tb.name}\n"
            f"Line No       : {tb.lineno}\n"
            f"Error Type    : {type(e).__name__}\n"
            f"Error Message : {str(e)}\n"
            f"------------------------------\n"
        )
        logger.error(log_message)
        logger.debug("Full Traceback:\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__)))
        raise
