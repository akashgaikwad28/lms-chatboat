# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"message": "Hello Radhyeee I Love You"}


# ??????????????????????????????????????????????????


from fastapi import FastAPI, Request
from chains.faq_chain import run_faq_chain
from chains.course_recommender import run_course_recommender
from agents.lms_agent import decide_and_route
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "LMS Chatbot is running 🚀"}

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    query = body.get("query")

    if not query:
        return {"success": False, "error": "Query is missing."}

    # Route to appropriate chain using agent
    response = await decide_and_route(query)
    return {"success": True, "response": response}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
