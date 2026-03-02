# CHain of Thought Prompting

import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
from pydantic import BaseModel, Field
from typing import Optional

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def detect_object(object: str):
    return f"{object} detected at 12,24 coordinates"

def navigate(coordinates: str):
    return f"Navigating to the destination {coordinates} coordinates"

def manipulate(object: str):
    return f"Manipulating {object} at 12,24 coordinates"

available_tools = {
    "detect_object": detect_object,
    "navigate": navigate,
    "manipulate": manipulate
}

SYSTEM_PROMPT = f"""
You are an expert AI Assistant in resolving user queries using chain of thought.
You are a robot brain that has to take inputs from the user and perform actions to achieve the user's goal.
You work on START, PLAN, TOOL, OBSERVE and OUTPUT steps.
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
- detect_object(object: str): Detects the object mentioned in the input in the environment.
- navigate(coordinates: str): Navigates to the destination mentioned in the input. This node is used
- manipulate(object: str): Manipulates the object mentioned in the input.

Example 1:
START: Hey, Can you navigate to the kitchen?
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
START: Hey, Can you pick up the pen on the table?

PLAN: {{"step": "PLAN",
"content": "Seems like the user is interested in picking up the pen on the table"}}
PLAN: {{"step": "PLAN",
"content": "Let's see if we have any available tool from the list of available tools."}}
PLAN: {{"step": "PLAN",
"content": "We have the detect_object tool available. So, we will call it to detect the object on the table."}}
PLAN: {{"step": "PLAN",
"content": "I need to call detect_object tool for pen as the input for object."}}
TOOL: {{"step": "TOOL", "tool": "detect_object", "input": "pen"}}
TOOL: {{"step": "OBSERVE", "tool": "detect_object", "output": "pen detected at 23,35 coordinates"}}
PLAN: {{"step": "PLAN",
"content": "Great, I got the pen detected at 23,35 coordinates"}}
PLAN: {{"step": "PLAN",
"content": "Let's see if we have any available tool from the list of available tools."}}
PLAN: {{"step": "PLAN",
"content": "We have the navigate tool available. So, we will call it to navigate to the 23,35 coordinates."}}
TOOL: {{"step": "TOOL", "tool": "navigate", "input": "23,35"}}
TOOL: {{"step": "OBSERVE", "tool": "navigate", "output": "Navigating to the 23,35 coordinates"}}
PLAN: {{"step": "PLAN",
"content": "Great, I navigated to the 23,35 coordinates"}}
PLAN: {{"step": "PLAN",
"content": "We have the manipulate tool available. So, we will call it to manipulate the pen at 23,35 coordinates."}}
TOOL: {{"step": "TOOL", "tool": "manipulate", "input": "pen"}}
TOOL: {{"step": "OBSERVE", "tool": "manipulate", "output": "Manipulating pen at 23,35 coordinates"}}
PLAN: {{"step": "PLAN",
"content": "Great, I manipulated the pen at 23,35 coordinates"}}
OUTPUT: {{"step": "OUTPUT",
"content": "The pen is picked up at 23,35 coordinates"}}

Example 3:
START: Hey, Can you pick up the bottle on the table?
PLAN: {{"step": "PLAN",
"content": "Seems like the user is interested in picking up the bottle on the table"}}
PLAN: {{"step": "PLAN",
"content": "Let's see if we have any available tool from the list of available tools."}}
PLAN: {{"step": "PLAN",
"content": "We have the detect_object tool available. So, we will call it to detect the object on the table."}}
PLAN: {{"step": "PLAN",
"content": "I need to call detect_object tool for bottle as the input for object."}}
TOOL: {{"step": "TOOL", "tool": "detect_object", "input": "bottle"}}
TOOL: {{"step": "OBSERVE", "tool": "detect_object", "output": "bottle detected at 12,24 coordinates "}}
PLAN: {{"step": "PLAN",
"content": "Great, I got the bottle detected at 12,24 coordinates"}}
PLAN: {{"step": "PLAN",
"content": "Let's see if we have any available tool from the list of available tools."}}
PLAN: {{"step": "PLAN",
"content": "We have the navigate tool available. So, we will call it to navigate to the 12,24 coordinates."}}
TOOL: {{"step": "TOOL", "tool": "navigate", "input": "12,24"}}
TOOL: {{"step": "OBSERVE", "tool": "navigate", "output": "Navigating to the 12,24 coordinates"}}
PLAN: {{"step": "PLAN",
"content": "Great, I navigated to the 12,24 coordinates"}}
PLAN: {{"step": "PLAN",
"content": "We have the manipulate tool available. So, we will call it to manipulate the bottle at 12,24 coordinates."}}
TOOL: {{"step": "TOOL", "tool": "manipulate", "input": "bottle"}}
TOOL: {{"step": "OBSERVE", "tool": "manipulate", "output": "Manipulating bottle at 12,24 coordinates"}}
PLAN: {{"step": "PLAN",
"content": "Great, I manipulated the bottle at 12,24 coordinates"}}
OUTPUT: {{"step": "OUTPUT",
"content": "The bottle is picked up at 12,24 coordinates"}}
"""

print("\n\n\n")

class MyOutputFormat(BaseModel):
    step: str = Field(..., description="The ID of the step. Example: PLAN, OUTPUT, TOOL, START, OBSERVE etc.")
    content: Optional[str] = Field(None, description="The content of the step.")
    tool: Optional[str] = Field(None, description="The tool to be called. Example: get_weather")
    input: Optional[str] = Field(None, description="The input to be passed to the tool. Example: delhi")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]
user_query = input("=> ")
message_history.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.parse(
        model="gpt-4o",
        response_format=MyOutputFormat,
        messages=message_history
    )
    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})

    parsed_result = response.choices[0].message.parsed
    
    if parsed_result.step == "START":
        print("Starting LLM Loop ==>", parsed_result.content)
        continue
    if parsed_result.step == "TOOL":
        tool_to_call = parsed_result.tool
        tool_input = parsed_result.input
        print(f"Calling tool: {tool_to_call} with input: {parsed_result.input}")

        tool_response =available_tools[tool_to_call](tool_input)
        print(f"Tool response: {tool_response}")
        message_history.append({"role": "developer", "content": json.dumps(
            {"step": "OBSERVE", "tool": tool_to_call, "input": tool_input, "output": tool_response}
        )})
        continue

    if parsed_result.step == "PLAN":
        print("Planning ==>", parsed_result.content)
        continue
    if parsed_result.step == "OUTPUT":
        print("Output ==>", parsed_result.content)
        break
print("\n\n\n")