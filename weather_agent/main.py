from openai import OpenAI
import os
import requests
from dotenv import load_dotenv

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

def main():
    user_query = input("> ")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": user_query
            }
        ]
    )
    print(f"Assistant: {response.choices[0].message.content}")


main()