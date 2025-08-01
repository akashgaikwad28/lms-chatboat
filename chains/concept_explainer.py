# chains/concept_explainer.py

from langchain_core.prompts import ChatPromptTemplate
from utils.llm_provider import get_llm
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        return response.content.strip()
    except Exception as e:
        logger.error(f"Concept explanation failed: {e}", exc_info=True)
        return "⚠️ Sorry, I couldn't explain that concept right now. Try again later."
