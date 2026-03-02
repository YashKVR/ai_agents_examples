import asyncio
import speech_recognition as sr
from openai import OpenAI
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
async_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def tts(speech: str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        instructions="Always speak in cheerful manner, with full of happiness and enthusiasm.",
        input=speech,
        response_format="pcm"
    ) as response:
        await LocalAudioPlayer().play(response) 

def main():
    r = sr.Recognizer() # Initialize the recognizer
    with sr.Microphone() as source: # Use the microphone as the source
        r.adjust_for_ambient_noise(source) # Adjust for ambient noise
        r.pause_threshold = 2 # Pause threshold
        print("Listening, please speak...")
        audio = r.listen(source) # Listen to the audio

        print("Processing audio...")
        stt = r.recognize_google(audio)

        print(f"You said: {stt}")
        SYSTEM_PROMPT = """
        You are an expert voice agent. You are given the transcript of what user has said using voice.
        You need to output as if you are an voice agent and whatever you speak will be converted back to audio and played back to user.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": stt}
            ]
        )
        print(f"Assistant: {response.choices[0].message.content}")
        asyncio.run(tts(speech=response.choices[0].message.content))

main()