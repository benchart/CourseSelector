import ollama
import requests
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def add_two_numbers(a: int, b: int) -> int:
  """
  Add two numbers

  Args:
    a: The first integer number
    b: The second integer number

  Returns:
    int: The sum of the two numbers
  """
  return a + b

def sub_two_numbers(a: int, b: int) -> int:
  """
  Sub two numbers

  Args:
    a: The first integer number
    b: The second integer number

  Returns:
    int: The difference of the two numbers
  """
  return a - b

def get_random_joke():
    """
    Fetches a random joke from an API.

    Returns:
    str: A string containing a joke, or an error message
    """
    logging.info("Fetching a random joke")
    joke_url = "https://official-joke-api.appspot.com/random_joke"

    try:
        response = requests.get(joke_url)
        response.raise_for_status()
        joke_data = response.json()
        joke = f"{joke_data['setup']} - {joke_data['punchline']}"
        logging.info(f"Random joke: {joke}")
        return joke
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while fetching joke: {str(e)}")
        return f"An error occurred while fetching a joke: {str(e)}"



response = ollama.chat(
  'mistral',
  messages=[{'role': 'user', 'content': 'tell me a random joke'}],
  tools=[add_two_numbers, sub_two_numbers, get_random_joke], # Actual function reference
)

print(response)

available_functions = {
  'add_two_numbers': add_two_numbers,
  'get_random_joke': get_random_joke,
  'sub_two_numbers': sub_two_numbers
}

for tool in response.message.tool_calls or []:
  function_to_call = available_functions.get(tool.function.name)
  if function_to_call:
    print('Function output:', function_to_call(**tool.function.arguments))
  else:
    print('Function not found:', tool.function.name)