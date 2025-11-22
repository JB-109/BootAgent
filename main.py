import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key="AIzaSyBek-wGgTymsHwVez338nw28Hd6zJHjIKU")

#++++++++++

if len(sys.argv) > 1:
    prompt = sys.argv[1]
else:
    prompt = input("How can I help you now? ")

if not prompt or not prompt.strip():
    print("Please provide a prompt!")
    sys.exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]
#++++++++++

response = client.models.generate_content(
    model='gemini-2.0-flash', contents=messages
)

print(response.text)
usage = response.usage_metadata

print(f"Prompt tokens: {usage.prompt_token_count}")
print(f"Response tokens: {usage.candidates_token_count}")

