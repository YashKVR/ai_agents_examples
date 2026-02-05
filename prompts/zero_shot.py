# Zero Shot Prompting

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
    )

# Zero Shot Prompting: Directly giving the instructions to the model
SYSTEM_PROMPT = "You should only and only answer the coding related questions. Do not answer any other questions. Your name is Alexa. If user asks something other than coding, just say sorry."

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Can you write a python code to print 'Hello, World!'?"
        }
    ]
)
print(response.choices[0].message.content)

# Zero Shot Prompting: The model is given a direct question or task without prioir examples.