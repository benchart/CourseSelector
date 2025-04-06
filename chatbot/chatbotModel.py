import ollama
import requests
import logging
from core.userManagement import UserManagement
from courseSelector import CourseSelector
import os
import ollama

# If you need to use a custom port
os.environ["OLLAMA_HOST"] = "http://localhost:11434"


#if you want to see logging, uncomment
#logging.basicConfig(level=logging.INFO,
                    #format='%(asctime)s - %(levelname)s - %(message)s')

class ChatbotModel:

    def __init__(self):
        self.management = UserManagement("studentData.txt", "adminData.txt")
        self.courseSelector = CourseSelector("core/courseDatabase.txt")

    @staticmethod
    def is_ollama_running():
        try:
            r = requests.get("http://localhost:11434")
            return r.status_code == 200
        except:
            return False

    management = UserManagement("studentData.txt", "adminData.txt")
    courseSelector = CourseSelector("core/courseDatabase.txt")
    
    #ollama joke generator I found online as testing, but we like it so we'll keep it in
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
        Used for a basic chat response to the user's query. Use when the query does not fit any other tool descriptions 

        Argument: 
            prompt: The input prompt that was originally input by the user
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

    #used for execution of chatbot commands

    def callChatbot(self, prompt: str) -> str:
        try:
            response = ollama.chat(
                model='llama3.2',
                messages=[{"role": "user", "content": prompt}],
                tools=[
                    self.get_random_joke,
                    self.does_not_match,
                    self.management.findUser,
                    self.courseSelector.filterClassesMaster
                ]
            )
            print(response)

            available_functions = {
                'get_random_joke': self.get_random_joke,
                'does_not_match': self.does_not_match,
                'findUser': self.management.findUser,
                'filterClassesMaster': self.courseSelector.filterClassesMaster
            }

            result = ""

            if response.message.tool_calls:
                for tool in response.message.tool_calls or []:
                    function_to_call = available_functions.get(tool.function.name)
                    if function_to_call:
                        try:
                            args = tool.function.arguments or {}
                            function_output = function_to_call(**args)
                            result += f"{function_output}\n"
                        except Exception as e:
                            result += f"⚠️ Error calling `{tool.function.name}`: {e}\n"
                    else:
                        result += f"❓ Unknown tool: {tool.function.name}\n"
            else:
                result = response.message.content  # Fallback to assistant's actual message

            print(result)
            return result
        
        except Exception as e:
            print("❌ Ollama call error:", e)
            return "❌ Internal server error — check terminal for details."