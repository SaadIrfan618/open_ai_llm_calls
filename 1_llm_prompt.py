from openai import OpenAI
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Access environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "what is the capital of japan"
        }
    ]
)

# print(completion)
print(completion.choices[0].message)
