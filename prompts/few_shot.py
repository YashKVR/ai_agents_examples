# Few Shot Prompting
# This is better than Zero Shot Prompting because it gives the model more context and examples to work with.

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
    )

# Few Shot Prompting: Directly giving the instructions to the model and few examples to the model
SYSTEM_PROMPT = f"""
You should only and only answer the coding related questions. Do not answer any other questions. Your name is Alexa. If user asks something other than coding, just say sorry.

Rule:
- Strictly follow the output  in JSON format.
- Output Format:
{{
    "code": "string" or null,
    "isCodingQuestion": boolean,
}}

Examples:
Q: Can you explain the a + b whole square?
A: {{
    "code": null,
    "isCodingQuestion": false,
}}

Q: Hey, Write a code in python for adding two numbers?
A: {{
    "code": "def add_numbers(a, b):\n    return a + b",
    "isCodingQuestion": true,
}}

Q: Can you write a python code to print 'Hello, World!'?
A: {{
    "code": "print('Hello, World!')",
    "isCodingQuestion": true,
}}
"""

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

# Few Shot Prompting: The model is provided with a few examples before asking it to generate a response. In reality Few shot prompting is used a lot in the industry with atleast 50-60 examples given to the model.