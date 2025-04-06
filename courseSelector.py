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
    def filterClassesMaster(self, catalogueNumMax: int, catalogueNumMin: int, class_code: list, creditMax: float, creditMin: float, instructorName: list, status: bool, subjectName: list, username: str = "user1"):
        """
        Master filtering function that filters courses based on multiple parameters
        such as credits, catalogue numbers, subject, class codes, etc.
        
        Arguments:
        - catalogueNumMax (int): The maximum catalogue number to filter by.
        - catalogueNumMin (int): The minimum catalogue number to filter by.
        - class_code (list): List of class codes to filter by.
        - creditMax (float): Maximum credits to filter by.
        - creditMin (float): Minimum credits to filter by.
        - instructorName (list): List of instructor names to filter by.
        - status (bool): Whether the user is an admin (True) or a student (False).
        - subjectName (list): List of subject names to filter by.
        - username (str): The username of the person making the request (default is 'user1').
        
        Returns:
        - list: A list of courses that match the provided filters.
        """
    
        # Provide default values for parameters that are None
        username = username if username is not None else "user1"
        subjectName = subjectName if subjectName is not None else []
        instructorName = instructorName if instructorName is not None else []
    
        # If catalogueNumMax or catalogueNumMin are None, set sensible default limits
        catalogueNumMax = catalogueNumMax if catalogueNumMax is not None else 9999
        catalogueNumMin = catalogueNumMin if catalogueNumMin is not None else 0
        creditMax = creditMax if creditMax is not None else 5
        creditMin = creditMin if creditMin is not None else 0

        # Start with the full list of courses
        self.courseData = self.readCourseList("courseDatabase.txt")
    
        # Apply filters in sequence
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
                    course_value = int(course[filter])  # Try converting to integer
                    if course_value >= numMin and course_value <= numMax:
                        # Proceed with your logic
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
        print(interestList)

        message = {'role': 'user', 'content': f'Assume you are an academic advisor. Based on this list of my interests ({interestList}, pick 15 classes from the list of potential classes in json notation ({self.courseData}) and explain why you have selected them. Match your selections as closely as possible to my interests. Make sure you pick exactly 15.)'}
        response_content = []
        print(message)

        for part in ollama.chat(model='llama3.2', messages=[message], stream=True):
            content = part['message']['content']
            #print(content, end='', flush=True)
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
        