from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agents.lms_agent import run_agent
import uvicorn

# FastAPI app initialization
app = FastAPI()

# Enable CORS (optional for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "LMS Chatbot is running 🚀"}

@app.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        user_query = body.get("user_query")
        user_id = body.get("user_id") # Optional user ID for tracking
        if not user_query:
            return {"success": False, "error": "Query is missing."}

        response = await run_agent(user_query, user_id)
        return {"success": True, "response": response}

    except Exception as e:
        return {"success": False, "error": str(e)}
    
@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
