import json
import ollama
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
    def filterClassesMaster(self, **kwargs):
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
        # Pull data from kwargs and ensure proper types
        username = kwargs.get('username', 'user1')

        # Handle 'null' values and convert them to None or appropriate default
        def handle_null(value, default=None):
            return default if value == 'null' or value is None else value

        catalogueNumMax = handle_null(kwargs.get('catalogueNumMax', 9999), 9999)
        catalogueNumMin = handle_null(kwargs.get('catalogueNumMin', 0), 0)
        creditMax = handle_null(kwargs.get('creditMax', 5), 5)
        creditMin = handle_null(kwargs.get('creditMin', 0), 0)

        class_code = kwargs.get('class_code', [])
        instructorName = kwargs.get('instructorName', [])
        status = kwargs.get('status', False)  # False is default for student status
        subjectName = kwargs.get('subjectName', [])

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
        self.findRelevantCoursesByInterest(username, status)

        return self.courseData






    #fetches course based on a specified parameter
    def _filterByType(self, parameterName: str, codeList: list) -> list[dict]:
        if codeList == []:
            return self.courseData
        
        newCourseList = []

        try:
            for course in self.courseData:
                for code in codeList:
                    if(code in course[parameterName]):
                        newCourseList.append(course)
                        break
            return newCourseList
        except KeyError:
            print(F"parameter not found: {KeyError}")

    #filters classes based on specified num range:
    def _filterByNum(self, filter: str, numMin: float, numMax: float) -> list[dict]:
        newCourseList = []

        try:
            for course in self.courseData:
                try:
                    course_value = float(course[filter])

                    if course_value >= numMin and course_value <= numMax:
                        newCourseList.append(course)
                except ValueError:
                    print(f"Invalid value for {filter}: {course[filter]}. Skipping this course.")
            return newCourseList
        
        except KeyError:
            print(F"Error occured: {KeyError}")

    #finds relevant classes based on the interest list
    def findRelevantCoursesByInterest(self, username: str, status: bool):
        if(username == ""):
            return []
        
        interestList = CourseSelector._matchInterests(UserManagement.findUser(username, status))
        print(f"Interest List: {interestList}")


        message = {
            'role': 'user', 
            'content': f'Assume you are an academic advisor. Based on this list of my interests {interestList}, pick 15 classes from the list of potential classes and explain why you have selected them. Match your selections as closely as possible to my interests. Make sure you pick exactly 15. {self.courseData}'
        }

        response_content = []
        print(message)

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

    def getCourseData(self) -> list[dict]:
        return self.courseData
        