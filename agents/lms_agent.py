from chains.course_recommender import run_course_recommender_chain
from chains.faq_chain import run_faq_chain
from langchain_core.prompts import ChatPromptTemplate

from utils.llm_provider import get_llm  # ✅ Use the helper

llm = get_llm()  # ✅ Initialize correctly

# Basic prompt to classify user intent
intent_prompt = ChatPromptTemplate.from_template("""
You are a smart assistant that classifies user queries into one of the following intents:
- "recommendation": if the user wants course suggestions or guidance.
- "faq": if the user is asking general questions about the platform (e.g., pricing, support, how to use).
- "other": if it’s unrelated or unknown.

User query: "{query}"
Your response (only one word - recommendation / faq / other):
""")

async def classify_intent(user_query: str) -> str:
    chain = intent_prompt | llm
    response = await chain.ainvoke({"query": user_query})
    intent = response.content.strip().lower()
    return intent


async def run_agent(user_query: str, user_id: str = None) -> str:
    """
    Main chatbot brain. Uses Gemini to classify the intent and routes the query.
    """
    intent = await classify_intent(user_query)

    if intent == "recommendation":
        return await run_course_recommender_chain(user_query, user_id)
    
    elif intent == "faq":
        return await run_faq_chain(user_query)
    
    else:
        return "🤖 Sorry, I couldn’t understand your query. Please try asking about a course or an FAQ."
