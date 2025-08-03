from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agents.lms_agent import run_agent
import uvicorn
import logging

# -----------------------------
# Logging configuration
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

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
    return {"message": "LMS Chatbot is running "}

@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        user_query = body.get("user_query")
        user_id = body.get("user_id")
        user_name = body.get("user_name")

        logger.info(f"Received chat request: query='{user_query}', user_id='{user_id}', user_name='{user_name}'")

        if not user_query:
            logger.warning("Query missing in request body.")
            return {"success": False, "error": "Query is missing."}

        response = await run_agent(user_query, user_id=user_id, user_name=user_name)

        logger.info(f"Response generated: {response}")
        return {"success": True, "response": response}

    except Exception as e:
        logger.error(f"Error processing /chat request: {e}", exc_info=True)
        return {"success": False, "error": str(e)}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
