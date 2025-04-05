import ollama
import requests
import logging
from core.userManagement import UserManagement
#from interests import INTEREST_OPTIONS, course_descriptions

#logging.basicConfig(level=logging.INFO,
                    #format='%(asctime)s - %(levelname)s - %(message)s')

class ChatbotModel:

    management = UserManagement("studentData.txt", "adminData.txt")

    def get_random_joke(self, prompt: str):
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
    
    #used for any excess queries that don't match any other function
    def does_not_match(self, prompt: str) -> str:
        """
        To be used when the query does not match any other tool functions

        Argument: 
            prompt: The input prompt that was not recognized
        Returns:
            str: A message telling the user they have entered an invalid query
        """
        message = {'role': 'user', 'content': prompt}
        response_content = []

        for part in ollama.chat(model='llama3.2', messages=[message], stream=True):
            content = part['message']['content']
            #print(content, end='', flush=True)
            response_content.append(content)

        return ''.join(response_content)
    
    #return matching class by their description
    def getByDescription(self) -> str:
        """
        Provides a description for every class available to the user

        Returns:
            str: A message telling the user they have successfully described each class
        """
        return "hello"

    #used for execution of chatbot commands
    def callChatbot(self, prompt: str):
        response = ollama.chat('llama3.2', messages=[
            {'role': 'user', 'content': prompt}],
            tools=[self.get_random_joke, self.getByDescription, self.does_not_match, self.management.findUser]
        )
        print(response)
        available_functions = {
            'get_random_joke': self.get_random_joke,
            'getByDescription': self.getByDescription,
            'does_not_match': self.does_not_match,
            'findUser': self.management.findUser
        }

        if response.message.tool_calls:
            for tool in response.message.tool_calls or []:
                function_to_call = available_functions.get(tool.function.name)
                if function_to_call:
                    print('Function output:', function_to_call(**tool.function.arguments)+"\n")
                else:
                    print('Function not found:', tool.function.name+"\n")
        else:
            logging.warning("No valid tool was called. This could be because the input was not understood.\n")