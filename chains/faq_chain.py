from langchain_core.prompts import ChatPromptTemplate
from utils.llm_provider import get_llm
from utils.logger import get_logger
import traceback

logger = get_logger(name="faq_chain")
llm = get_llm()

faq_prompt = ChatPromptTemplate.from_template("""
You are a support assistant for **Acash Tech**, an online LMS platform. Answer user questions clearly and in a friendly tone.

Only respond based on facts about Acash Tech or general LMS behavior.

Answer the student's question clearly and politely using the following FAQs as your reference:

FAQs:
1. How do I enroll in a course? → You can log in, go to the courses page, and click “Enroll” or “Buy Now”.
2. What payment methods are supported? → We support PayPal and credit/debit cards.
3. Can I track my course progress? → Yes, go to "My Courses" and see your progress.
4. What if I forget my password? → Click "Forgot password" on the login page.
5. Can I contact the course instructor? → Yes, each course page has a contact form.
6. How do I reset my course progress? → Go to "My Courses" → "Settings" → "Reset Progress".
7. Can I get a refund? → Yes, within 7 days of purchase if less than 30% of course completed.

Student Question: "{user_question}"

Give a helpful, student-friendly response.
""")

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
