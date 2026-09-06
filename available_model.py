import requests
import os
from dotenv import load_dotenv
from groq import Groq
import json

# 1. Load environment variables from the .env file
load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
data = response.json()
with open("api_response.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)