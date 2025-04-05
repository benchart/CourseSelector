import ollama
import requests
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ChatbotModel:
    
    def add_two_numbers(self, a: int, b: int) -> int:
        """
        Add two numbers

        Args:
            a: The first integer number
            b: The second integer number

        Returns:
            int: The sum of the two numbers
        """
        return a + b

    def sub_two_numbers(self, a: int, b: int) -> int:
        """
        Sub two numbers

        Args:
            a: The first integer number
            b: The second integer number

        Returns:
            int: The difference of the two numbers
        """
        return a - b

    def get_random_joke(self):
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
        
    def does_not_match(self) -> str:
        """
        To be used when the query does not match any other tool functions

        Returns:
            str: A message telling the user they have entered an invalid query
        """
        return "Invalid Query"
    
    def callChatbot(self, prompt: str):
        # Use functools.partial to bind the methods to the current instance
        add_two_numbers_tool = self.add_two_numbers
        sub_two_numbers_tool = self.sub_two_numbers
        get_random_joke_tool = self.get_random_joke
        does_not_match_tool = self.does_not_match

        # Now pass the wrapped functions (partial functions)
        response = ollama.chat('llama3.2', messages=[
            {'role': 'user', 'content': prompt}],
            tools=[add_two_numbers_tool, sub_two_numbers_tool, get_random_joke_tool, does_not_match_tool]
        )

        print(response)

        available_functions = {
            'add_two_numbers': self.add_two_numbers,
            'get_random_joke': self.get_random_joke,
            'sub_two_numbers': self.sub_two_numbers,
            'does_not_match': self.does_not_match
        }

        if response.message.tool_calls:
            for tool in response.message.tool_calls or []:
                function_to_call = available_functions.get(tool.function.name)
                if function_to_call:
                    print('Function output:', function_to_call(**tool.function.arguments))
                else:
                    print('Function not found:', tool.function.name)
        else:
            logging.warning("No valid tool was called. This could be because the input was not understood.")



model = ChatbotModel()
model.callChatbot("hello")