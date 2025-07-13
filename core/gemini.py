from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

def request_gemini(contests:str):
    try:
        response = client.models.generate_content(model="gemini-2.5-flash",contents=contests)
        print(response)
        return response.text
    except Exception as e:
        return "Something went wrong"

