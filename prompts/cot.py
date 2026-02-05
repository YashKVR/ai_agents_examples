# CHain of Thought Prompting

import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = f"""
You are an expert AI Assistant in resolving user queries using chain of thought.
You work on START,THINK, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an output.

Rules:
- Strictly follow the given JSON output format.
-Only run one step at a time.
-The sequence of steps is START(where user gives an input), PLAN(That can be multiple times) and finally OUTPUT(which is going to be displayed to the user)

Output JSON Format:
{{
    "step": "START" | "PLAN" | "OUTPUT",
    "content": "string"
}}

Example:
START: Hey, Can you solve 2 + 3 * 10 / 5
PLAN: {{"step": "PLAN",
"content": "Seems like the user is interested in Maths problem"}}
PLAN: {{"step": "PLAN",
"content": "Looking at the problem, we should solve this using BODMAS method"}}
PLAN: {{"step": "PLAN",
"content": "Yes, the BODMAS is correct thing to be done here."}}
PLAN: {{"step": "PLAN",
"content": "first we must divide 10 by 5 to get 2"}}
PLAN: {{"step": "PLAN",
"content": "then we must multiply 3 by 2 to get 6"}}
PLAN: {{"step": "PLAN",
"content": "then we must add 2 and 6 to get 8"}}
PLAN: {{"step": "PLAN",
"content": "finally we must return the result as 8"}}
OUTPUT: {{"step": "OUTPUT",
"content": "8"}}

"""

print("\n\n\n")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]
user_query = input("=> ")
message_history.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=message_history
    )
    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})

    parsed_result = json.loads(raw_result)
    
    if parsed_result["step"] == "START":
        print("Starting LLM Loop ==>", parsed_result.get("content"))
        continue
    if parsed_result["step"] == "PLAN":
        print("Planning ==>", parsed_result.get("content"))
        continue
    if parsed_result["step"] == "OUTPUT":
        print("Output ==>", parsed_result.get("content"))
        break
print("\n\n\n")