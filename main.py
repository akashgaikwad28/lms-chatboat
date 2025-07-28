# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"message": "Hello Radhyeee I Love You"}


# ??????????????????????????????????????????????????


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agents.lms_agent import decide_and_route
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
        query = body.get("query")

        if not query:
            return {"success": False, "error": "Query is missing."}

        response = await decide_and_route(query)
        return {"success": True, "response": response}

    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
