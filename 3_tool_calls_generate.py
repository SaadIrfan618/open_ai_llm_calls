import json
import os
import random
from textwrap import dedent

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

# Load the .env file
load_dotenv()

# Access environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

MODEL = "gpt-4o-mini"


class ValidationError(Exception):
    pass


# define function/functions llm can call
# 1. create a "tools" list; this will be a List[Dict]; each dict defines a function

# 2. each dict will have two keys; a) type: function
#                                  b) function: Dict

# 3. each function dict will also have two keys a) name: name of function to call
#                                               b) description: description of function
#                                               c) parameters: Dict

# 4. each parameter dict will also have two keys a) type: what to return (function args as a dict) so 'object'
#                                                b) properties: Dict
#                                                c) force to follow provided schema by required(list of arguments,
#                                                   strict:True and additionalParameters:False)

# 5. each property dict will also info about func arguments a) 'name of argument': {'type': 'Datatype', 'description':'text'}

tools = [
    {
        "type": "function",
        "function": {
            "name": "add_to_a_rand_number",
            "description": "Takes in an integer as an argument",
            "parameters": {
                "type": "object",
                "properties": {
                    "number_to_add": {"type": "integer", "description": "Any integer"}
                },
                "required": ["number_to_add"],
                "strict": True,
                "additionalProperties": False,
            },
        },
    }
]


messages = []
detailed_prompt = """
        the user has a function that requires a random integer. Your job is to select an integer according to
        user input and return the tool call
        """
messages.append({"role": "system", "content": dedent(detailed_prompt)})
messages.append({"role": "user", "content": "Choose a random number between 10 and 15"})

completion = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=tools,
)

# print(completion)
print("Finish reason: ", completion.choices[0].finish_reason)  # must be tool_calls
print("Refusal: ", completion.choices[0].message.refusal)  # must be None

function_id = completion.choices[0].message.tool_calls[0].id
print("Function to call id: ", function_id)

function_name = completion.choices[0].message.tool_calls[0].function.name
print("Function to call: ", function_name)

if function_name == "add_to_a_rand_number":
    argument_dict = json.loads(
        completion.choices[0].message.tool_calls[0].function.arguments
    )
    number_to_add = int(argument_dict["number_to_add"])

# can validate with such code as well:
function_names_args = ["add_to_a_rand_number", "number_to_add"]
if function_name in function_names_args:
    for function_argument, value in argument_dict.items():
        if function_argument not in function_names_args:
            raise ValidationError("Wrong Argument")
else:
    raise ValidationError("Wrong Function name")

# using function call to run a function


def add_to_a_rand_number(number_to_add: int) -> int:
    """takes a number and adds it to a random generated integer

    Args:
        number_to_add (int): user provides number

    Returns:
        int: user provided number + random integer
    """
    int_a = random.randint(0, 100)
    print("Random number is: ", int_a)
    print("user number is: ", number_to_add)
    return int_a + number_to_add


if function_name == "add_to_a_rand_number":
    results = add_to_a_rand_number(number_to_add)
    print("Function result is: ", results)


# if use an llm node to generate a tool call, get a tool call and run function
# want to send back result of function just called to same llm node
# use tool role eg:
# messages.append({
#     "role":"tool",
#     "tool_call_id":tool_call_id,
#     "name": tool_function_name,
#     "content":results
# })

# Newer models such as gpt-4o or gpt-3.5-turbo can call multiple functions in one turn.
