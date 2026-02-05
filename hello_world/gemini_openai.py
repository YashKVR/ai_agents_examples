import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
    )
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role": "system",
            "content": "You are an expert in Maths and only and only answer questions related to Maths."
        },
        {
            "role": "user",
            "content": "What is x^2 + 2x + 1 = 0?"
        }
    ]
)
print(response.choices[0].message.content)