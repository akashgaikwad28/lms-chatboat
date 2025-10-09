from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agents.lms_agent import run_agent
from utils.logger import get_logger
import uvicorn
import traceback

logger = get_logger(name="main")

# -----------------------------
# FastAPI app initialization
# -----------------------------
app = FastAPI()

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    logger.info("Health check hit at '/' endpoint.")
    return {"message": "LMS Chatbot is running"}

@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        user_query = body.get("user_query")
        user_id = body.get("user_id")
        user_name = body.get("user_name")

        logger.info(f"[Chat Request] query='{user_query}', user_id='{user_id}', user_name='{user_name}'")

        if not user_query:
            logger.warning("[Chat Request] Missing 'user_query' in request body.")
            return {"success": False, "error": "Query is missing."}

        response = await run_agent(user_query, user_id=user_id, user_name=user_name)

        logger.info(f"[Chat Response] {response}")
        return {"success": True, "response": response}

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)[-1]
        logger.error(
            f"\n--- Exception in /chat endpoint ---\n"
            f"File      : {tb.filename}\n"
            f"Function  : {tb.name}\n"
            f"Line No   : {tb.lineno}\n"
            f"Error     : {type(e).__name__} - {str(e)}\n"
            f"------------------------------------"
        )
        logger.debug("Full Traceback:\n" + "".join(traceback.format_exception(type(e), e, e.__traceback__)))
        return {"success": False, "error": "Internal Server Error"}

@app.get("/health")
def health_check():
    logger.info("Health check hit at '/health' endpoint.")
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
