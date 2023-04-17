import openai
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")



def generate(prompt):
    """
    Generates a text completion for a given prompt using the OpenAI GPT-3 API.
    
    Args:
    - prompt (str): The text prompt to generate a completion for.
    
    Returns:
    - str: The generated text completion.
    """
    model_engine = "text-davinci-002"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text
    return message.strip()

def get_rating(x):
    """
    Extracts a rating from a string.
    
    Args:
    - x (str): The string to extract the rating from.
    
    Returns:
    - int: The rating extracted from the string, or None if no rating is found.
    """
    nums = [int(i) for i in re.findall(r'\d+', x)]
    if len(nums)>0:
        return min(nums)
    else:
        return None

# Summarize simulation loop with OpenAI GPT-4
def summarize_simulation(log_output):
    prompt = f"Summarize the simulation loop:\n\n{log_output}"
    response = generate(prompt)
    return response
