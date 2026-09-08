from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print("API Loaded:", api_key[:10] + "...")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-3.5-flash")

app = FastAPI()

chat_history = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/health")
def health():
    return {"status": "running"}

@app.post("/chat")
def chat(req: ChatRequest):

    global chat_history

    chat_history.append(f"User: {req.message}")

    prompt = f"""
    You are a helpful AI assistant.

    Conversation History:
    {chr(10).join(chat_history)}

    User: {req.message}
    """

    response = model.generate_content(prompt)

    ai_reply = response.text

    chat_history.append(f"Assistant: {ai_reply}")

    return {"reply": ai_reply}