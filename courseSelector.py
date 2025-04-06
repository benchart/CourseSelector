import json
import ollama
import re
from core.userManagement import UserManagement

INTEREST_OPTIONS = [
         "Math", "Creative Writing", "Biology", "Robotics", "Music Theory",
    "World History", "Computer Programming", "Environmental Science", "Public Speaking",
    "Theater Arts", "Astronomy", "Psychology", "Film Studies", "Chemistry",
    "Political Science", "Entrepreneurship", "Photography", "Philosophy", "Statistics",
    "Debate", "Forensic Science", "Sociology", "Graphic Design", "Economics",
    "Physics", "Marine Biology", "UX Design", "Digital Media", "AI",
    "Game Development", "Ethics", "Anthropology", "Web Development", "Linguistics",
    "Cognitive Science", "Marketing", "Botany", "Data Science", "Education Policy",
    "Foreign Languages", "Geology", "Journalism", "Music Performance", "Gender Studies",
    "Classical Studies", "Animation", "Social Work", "Nanotech", "Zoology"
    ]

class CourseSelector:

    userSystem = UserManagement("studentData.txt", "adminData.txt")
    courseData: list[dict]

    def __init__(self, databasePath: str):
        self.courseData = self.readCourseList(databasePath)


    #master filtering function, uses the whole courseData dictionary to provide the most complete course list
    def filterClassesMaster(self, **kwargs) -> str:
        """
        Master filtering function that filters courses based on multiple parameters
        such as credits, catalogue numbers, subject, class codes, etc.

        Arguments (now passed as keyword arguments):
        - catalogueNumMax (int): The maximum catalogue number to filter by.
        - catalogueNumMin (int): The minimum catalogue number to filter by.
        - class_code (list): List of class codes to filter by.
        - creditMax (float): Maximum credits to filter by.
        - creditMin (float): Minimum credits to filter by.
        - instructorName (list): List of instructor names to filter by.
        - status (bool): Whether the user is an admin (True) or a student (False).
        - subjectName (list): List of subject names to filter by.
        - username (str): The username of the person making the request (default is 'user1').
        """
        
        # Handle 'null' values and convert them to None or appropriate default
        def handle_null(value, default=None):
            return default if value == 'null' or value is None or value == '' else value

        username = handle_null(kwargs.get('username', 'user1'), 'user1')
        catalogueNumMax = handle_null(kwargs.get('catalogueNumMax', 999999), 999999)
        catalogueNumMin = handle_null(kwargs.get('catalogueNumMin', 0), 0)
        creditMax = handle_null(kwargs.get('creditMax', 10), 10)
        creditMin = handle_null(kwargs.get('creditMin', 0), 0)

        class_code = kwargs.get('class_code', [])
        instructorName = kwargs.get('instructorName', [])
        status = kwargs.get('status', False)  # False is default for student status
        subjectName = kwargs.get('subjectName', [])

        # Sanitize class_code and subjectName inputs to handle extra data
        class_code = CourseSelector.sanitize_json_input(class_code) if isinstance(class_code, str) else class_code
        subjectName = CourseSelector.sanitize_json_input(subjectName) if isinstance(subjectName, str) else subjectName


        # Convert values to appropriate types
        try:
            catalogueNumMax = int(catalogueNumMax) if catalogueNumMax is not None else 9999
        except ValueError:
            catalogueNumMax = 9999

        try:
            catalogueNumMin = int(catalogueNumMin) if catalogueNumMin is not None else 0
        except ValueError:
            catalogueNumMin = 0

        try:
            creditMax = float(creditMax) if creditMax is not None else 5
        except ValueError:
            creditMax = 5

        try:
            creditMin = float(creditMin) if creditMin is not None else 0
        except ValueError:
            creditMin = 0

        # Ensure class_code and subjectName are lists, even if they are passed as strings
        class_code = json.loads(class_code) if isinstance(class_code, str) else class_code
        subjectName = json.loads(subjectName) if isinstance(subjectName, str) else subjectName
        instructorName = json.loads(instructorName) if isinstance(instructorName, str) else instructorName

        # Ensure these are lists (if they are passed as strings)
        if not isinstance(class_code, list):
            class_code = [class_code]  # If it's a single string, turn it into a list
        if not isinstance(subjectName, list):
            subjectName = [subjectName]  # Same here for subjectName
        if not isinstance(instructorName, list):
            instructorName = [instructorName]  # Same for instructorName

        # Ensure boolean for status (if it's a string)
        status = status.lower() == 'true' if isinstance(status, str) else status

        # Reload course data
        self.courseData = self.readCourseList("courseDatabase.txt")

        # Filter by parameters
        self.courseData = self._filterByNum('units', creditMin, creditMax)
        self.courseData = self._filterByNum('catalog_number', catalogueNumMin, catalogueNumMax)
        self.courseData = self._filterByType('instructor', instructorName)
        self.courseData = self._filterByType('subject', subjectName)
        self.courseData = self._filterByType('class_code', class_code)

        # After filtering based on the provided parameters, find relevant courses by interest
        print(self.findRelevantCoursesByInterest(username, status))
        return self.findRelevantCoursesByInterest(username, status)
        #return self.courseData






    #fetches course based on a specified parameter
    def _filterByType(self, parameterName: str, codeList: list) -> list[dict]:
        if codeList == [] or [None]:
            return self.courseData
        
        newCourseSet = set()
        try:
            for course in self.courseData:
                course_tuple = tuple(course.items())

                for code in codeList:
                    if(code in course[parameterName]):
                        newCourseSet.add(course_tuple)
                        break

            return [dict(course_tuple) for course_tuple in newCourseSet]
        
        except KeyError:
            print(F"parameter not found: {KeyError}")

    #filters classes based on specified num range:
    def _filterByNum(self, filter: str, numMin: float, numMax: float) -> list[dict]:
        newCourseSet = set()

        try:
            for course in self.courseData:
                try:
                    course_value = float(course[filter])
                    course_tuple = tuple(course.items())

                    if course_value is None or not isinstance(course_value, str):
                        newCourseSet.add(course_tuple)

                    if course_value >= numMin and course_value <= numMax:
                        newCourseSet.add(course_tuple)

                except ValueError:
                    print(f"Invalid value for {filter}: {course[filter]}. Skipping this course.")
            return [dict(course_tuple) for course_tuple in newCourseSet]
        
        except KeyError:
            print(F"Error occured: {KeyError}")

    #finds relevant classes based on the interest list
    def findRelevantCoursesByInterest(self, username: str, status: bool) -> str:

        interestList = CourseSelector._matchInterests(UserManagement.findUser(username, status))

        message = {
            'role': 'user', 
            'content': f'Assume you are my academic advisor. Based on this list of my interests {interestList}, pick 15 classes and explain why you have selected them. Match your selections as closely as possible to my interests. Use this data as your list of potential options: {self.courseData}'
        }

        response_content = []

        for part in ollama.chat(model='llama3.2', messages=[message], stream=True):
            content = part['message']['content']
            
            if not isinstance(content, str):
                content = str(content)

            response_content.append(content)
        return ''.join(response_content)

    #returns the matching interests from the interestIndicies list
    @staticmethod
    def _matchInterests(user: dict) -> list:
        interestList: list = []
        try:
            for index in user['interestIndicies']:
                interestList.append(INTEREST_OPTIONS[int(index)])
            return interestList
        except KeyError:
            print(f"Indicies not found: {KeyError}")
    
    #reads the course database
    @staticmethod
    def readCourseList(databasePath: str) -> dict:
        try:
            with open(databasePath, "r") as file:
                    json_data = file.readline()
                    try:
                        newJson = json.loads(json_data)
                        return newJson
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON: {e}")
        except FileNotFoundError as e:
            print(f"Filepath not found for {databasePath}")


    def sanitize_json_input(input_string: str) -> list:
        """
        This function will try to extract valid JSON from the input string,
        and ignore any non-JSON content that may follow (like 'Morning classes should be excluded.')
        """
        try:
            # Attempt to extract the part that looks like a JSON array
            match = re.match(r'(\[.*\])', input_string.strip())  # regex to extract array-like content
            if match:
                # Parse the valid JSON array found
                return json.loads(match.group(1))
            else:
                # If no valid JSON array is found, return an empty list
                return []
        except json.JSONDecodeError:
            # In case of an invalid JSON, return an empty list
            print(f"Error decoding JSON from input: {input_string}")
            return []


    def getCourseData(self) -> list[dict]:
        return self.courseData
        