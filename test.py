from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print("Key loaded:", api_key[:10] + "...")

genai.configure(api_key=api_key)

for model in genai.list_models():
    print(model.name)