# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"message": "Hello Radhyeee I Love You"}


# ??????????????????????????????????????????????????


# main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from agents.lms_agent import run_agent
from config.settings import settings

app = FastAPI()

class ChatRequest(BaseModel):
    query: str
    user_id: str = None

@app.post("/chat")
async def chat_with_bot(req: ChatRequest):
    response = await run_agent(req.query, req.user_id)
    return {"response": response}
