import ollama
import requests
import logging
from userManagement import UserManagement

#logging.basicConfig(level=logging.INFO,
                    #format='%(asctime)s - %(levelname)s - %(message)s')

class ChatbotModel:
    class_descriptions = [
    "Introduction to Computer Science: A foundational course in programming, algorithms, and problem-solving.",
    "Calculus I: Study of limits, derivatives, and integrals, focusing on single-variable functions.",
    "Psychology 101: An overview of the basics of psychology, including behavioral science, cognition, and development.",
    "Introduction to Philosophy: Exploration of major philosophical ideas, thinkers, and ethical dilemmas.",
    "Chemistry 101: Basic principles of chemistry, including atomic structure, chemical reactions, and stoichiometry.",
    "Microeconomics: Introduction to economic theory, including supply and demand, market structures, and government intervention.",
    "World History: Survey of major events and developments from ancient to modern times across different cultures.",
    "Statistics for Social Sciences: Introduction to statistics with applications in social research and data analysis.",
    "English Literature: Study of classic and contemporary works of fiction, poetry, and drama from various cultures.",
    "Introduction to Sociology: Exploration of social structures, institutions, and processes that shape human behavior.",
    "Biology 101: Fundamentals of biology, including cell biology, genetics, and ecological systems.",
    "Public Speaking: Develop skills in delivering persuasive, informative, and effective speeches.",
    "Physics I: Introduction to the fundamental concepts of physics, including mechanics, motion, and energy.",
    "Business Management: Study of business principles, including leadership, strategic planning, and organizational behavior.",
    "Art History: Survey of the evolution of art from prehistoric times to the present, focusing on different periods and movements.",
    "Advanced Calculus: A deeper dive into multi-variable calculus and its applications in real-world scenarios.",
    "Environmental Science: Examination of ecological systems, environmental challenges, and sustainable practices.",
    "Political Science 101: Introduction to political theory, systems, and institutions at the national and global levels.",
    "Ethics in Technology: Exploration of the ethical challenges and dilemmas in the rapidly evolving tech industry.",
    "Creative Writing: A course designed to help students develop their writing skills in fiction, poetry, and creative non-fiction."
    ]

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
        return self.summarizeClass()
    
    #returns a description of a class
    def summarizeClass(self) -> str: 
        message = {'role': 'user', 'content': F"Give me the string array of one-word summarizations without explanation or other text:{self.class_descriptions}"}
        response_content = []

        for part in ollama.chat(model='llama3.2', messages=[message], stream=True):
            content = part['message']['content']
            #print(content, end='', flush=True)
            response_content.append(content)

        return ''.join(response_content)

    #used for execution of chatbot commands
    def callChatbot(self, prompt: str):
        response = ollama.chat('llama3.2', messages=[
            {'role': 'user', 'content': prompt}],
            tools=[self.add_two_numbers, self.sub_two_numbers, self.get_random_joke, self.getByDescription, self.does_not_match, UserManagement.findUser]
        )
        #print(response)
        available_functions = {
            'add_two_numbers': self.add_two_numbers,
            'get_random_joke': self.get_random_joke,
            'sub_two_numbers': self.sub_two_numbers,
            'getByDescription': self.getByDescription,
            'does_not_match': self.does_not_match,
            'UserManagement.findUser': UserManagement.findUser
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