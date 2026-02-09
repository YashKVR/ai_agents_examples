# CHain of Thought Prompting

import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import requests

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    headers = {"User-Agent": "curl/7.68.0"}
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    else:
        return f"Something went wrong.Error: {response.status_code}"

available_tools = {
    "get_weather": get_weather
}

SYSTEM_PROMPT = f"""
You are an expert AI Assistant in resolving user queries using chain of thought.
You work on START,THINK, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an output.
You can also call a tool if required from the list of available tools.
For every tool call wait for the observe step which is the output from the called tool.

Rules:
- Strictly follow the given JSON output format.
-Only run one step at a time.
-The sequence of steps is START(where user gives an input), PLAN(That can be multiple times) and finally OUTPUT(which is going to be displayed to the user)

Output JSON Format:
{{
    "step": "START" | "PLAN" | "OUTPUT" | "TOOL",
    "content": "string",
    "tool": "string" | null,
    "input": "string" | null,
}}

Available Tools:
- get_weather(city: str): Takes a city name as input and returns the weather information about that city.

Example 1:
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

Example 2:
START: What is the weather in Delhi?
PLAN: {{"step": "PLAN",
"content": "Seems like the user is interested in weather information"}}
PLAN: {{"step": "PLAN",
"content": "Let's see if we have any available tool from the list of available tools."}}
PLAN: {{"step": "PLAN",
"content": "We have the get_weather tool available. So, we will call it to get the weather information."}}
PLAN: {{"step": "PLAN",
"content": "I need to call get_weather tool for delhi as the input for city."}}
TOOL: {{"step": "TOOL", "tool": "get_weather", "input": "delhi"}}
TOOL: {{"step": "OBSERVE", "tool": "get_weather", "output": "The weather in Delhi is 20°C"}}
PLAN: {{"step": "PLAN",
"content": "Great, I got the weather information about Delhi"}}
OUTPUT: {{"step": "OUTPUT",
"content": "The weather in Delhi is 20°C"}}
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
    if parsed_result["step"] == "TOOL":
        tool_to_call = parsed_result.get("tool")
        tool_input = parsed_result.get("input")
        print(f"Calling tool: {tool_to_call} with input: {parsed_result.get('input')}")

        tool_response =available_tools[tool_to_call](tool_input)
        print(f"Tool response: {tool_response}")
        message_history.append({"role": "developer", "content": json.dumps(
            {"step": "OBSERVE", "tool": tool_to_call, "input": tool_input, "output": tool_response}
        )})
        continue

    if parsed_result["step"] == "PLAN":
        print("Planning ==>", parsed_result.get("content"))
        continue
    if parsed_result["step"] == "OUTPUT":
        print("Output ==>", parsed_result.get("content"))
        break
print("\n\n\n")