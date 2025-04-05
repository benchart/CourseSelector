import ollama
import requests
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

tools = [
    {
        "name": "get_random_joke",
        "description": "Get a random joke",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    }
]

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
        print("this is working")
        return joke
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while fetching joke: {str(e)}")
        return f"An error occurred while fetching a joke: {str(e)}"

print(get_random_joke())
for part in ollama.chat(model='mistral', messages=[{'role': 'user', 'content': 'get me a random joke'}], tools=tools, stream=True):
        print(part['message']['content'], end='', flush=True) 