import os

from dotenv import load_dotenv
from openai import OpenAI

# Load the .env file
load_dotenv()

# Access environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

# messages is a list of instructions to llm
# each element is a dict with two keys
# first key specifies whether instruction from user or for built-in system role
# second key is the content
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "what is the capital of japan"},
    ],
)

# The answer is completion
# A class whose components can be accessed by completion.key
# If want to choose an option within a key
# A class whose components can be accessed by completion.key[0].sub_key
# access any value from class it becomes string
# print(completion)
print("Refusal: ", completion.choices[0].message.refusal)  # should be None
print("Reason for end: ", completion.choices[0].finish_reason)  # should be stop
print("Answer: ", completion.choices[0].message.content)
