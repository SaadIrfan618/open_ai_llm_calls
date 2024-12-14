from openai import OpenAI
from dotenv import load_dotenv
import os
from textwrap import dedent
from pydantic import BaseModel

# Load the .env file
load_dotenv()

# Access environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI()

MODEL = "gpt-4o-mini"


class MathReasoning(BaseModel):
    class Step(BaseModel):
        explanation: str
        output: str

    steps: list[Step]
    final_answer: str


math_tutor_prompt = '''
    You are a helpful math tutor. You will be provided with a math problem,
    and your goal will be to output a step by step solution, along with a final answer.
    For each step, just provide the output as an equation use the explanation field to detail the reasoning.
'''


def get_math_solution(question: str):
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": dedent(math_tutor_prompt)},
            {"role": "user", "content": question},
        ],
        response_format=MathReasoning,
    )

    return completion.choices[0].message


question = "how can I solve 8x + 7 = -23"
result = get_math_solution(question).parsed

print(result)
print(result.steps)
print("Final answer:")
print(result.final_answer)
