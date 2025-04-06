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
    def filterClassesMaster(self, catalogueNumMax=None, catalogueNumMin=None, class_code=None, creditMax=None, creditMin=None, instructorName=None, status=False, subjectName=None, username=None):
        
        '''
        This function is used to filter out classes by a variety of parameters
        Always refer to the default parameters and thier type casting, do not input any NoneType values

        Arguments:
        username: The name of the user. Attempt to extrapolate but if not, resort to 'pork'
        status: this boolean value indicates whether or not the user is a student or an admin. If true, they are admin. If false, student.
        creditMin: the minimum number of credits prefered by the user
        creditMax: the maximum number of credits preferred by the user
        catalogueNumMin: the lowest catalogue number preferred by the user. Useful for determining if the user wants to take 100 level classes, or nothing lower than 300, for example.
        catalogueNumMax: the maximum catalogue number preffered by the user. Useful for determining the upper limit of difficulty for classes.
        instructorName: a list of names of instructors. Usually will be left blank unless specifically requested.
        subjectName: the list containing the name(s) of the subject the user is looking for.
        class_code: a list of class codes that the user is requesting.

        Once all of the relevant filtering algorithims have been run, findRelevantCourseByInterest runs in order to find the best suitable match for the student.
        '''


        catalogueNumMax = catalogueNumMax if catalogueNumMax is not None else 9999
        catalogueNumMin = catalogueNumMin if catalogueNumMin is not None else 0
        creditMax = creditMax if creditMax is not None else 5 
        creditMin = creditMin if creditMin is not None else 0 
        instructorName = instructorName if instructorName is not None else []
        status = status if status is not None else False
        subjectName = subjectName if subjectName is not None else []
        class_code = class_code if class_code is not None else []
        username = username if username is not None else "user1"

        self.courseData = self._filterByNum('units', creditMin, creditMax)
        self.courseData = self._filterByNum('catalog_number', catalogueNumMin, catalogueNumMax)
        self.courseData = self._filterByType('instructor', instructorName)
        self.courseData = self._filterByType('subject', subjectName)
        self.courseData = self._filterByType('class_code', class_code)

        self.findRelevantCoursesByInterest(username, status)



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
        