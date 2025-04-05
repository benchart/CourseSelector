import json
import ollama
from chatbot.chatbotModel import ChatbotModel
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

    model = ChatbotModel()
    userSystem = UserManagement("studentData.txt", "adminData.txt")
    courseData: list[dict]

    def __init__(self, databasePath: str):
        self.courseData = self.readCourseList(databasePath)


    #master filtering function, uses the whole courseData dictionary to provide the most complete course list
    def filterClassesMaster(self, username: str = "", status: bool = False, 
                            creditMin: float = 0, creditMax: float = 1.0,
                             catalogueNumMin: float = 0, catalogueNumMax: float = 500,
                             instructorName: list = [], subjectName: str = [], 
                             class_code: str = []):
        self.courseData = self.filterByNum('units', creditMin, creditMax)
        self.courseData = self.filterByNum('catalog_number', catalogueNumMin, catalogueNumMax)
        self.courseData = self.filterByType('instructor', instructorName)
        self.courseData = self.filterByType('subject', subjectName)
        self.courseData = self.filterByType('class_code', class_code)

        self.findRelevantCourseByInterest(username, status)







    #fetches course based on a specified parameter
    def filterByType(self, parameterName: str, codeList: list) -> list[dict]:
        if codeList == []:
            return self.courseData
        
        newCourseList = []

        try:
            for course in self.courseData:
                for code in codeList:
                    if(code in course[parameterName]):
                        newCourseList.append(course)
                        continue
            return newCourseList
        except KeyError:
            print(F"parameter not found: {KeyError}")

    #filters classes based on specified num range:
    def filterByNum(self, filter: str, numMin: float, numMax: float) -> list[dict]:
        newCourseList = []
        try:
            for course in self.courseData:
                if ((int(course[filter])) >= numMin and (int(course[filter])) <= numMax):
                    newCourseList.append(course)
            return newCourseList
        except KeyError:
            print(F"Error occured: {KeyError}")

    #finds relevant classes based on the interest list
    def findRelevantCoursesByInterest(self, username: str, status: bool):
        if(username == ""):
            return []
        interestList = CourseSelector.matchInterests(UserManagement.findUser(username, status))
        print(interestList)

        message = {'role': 'user', 'content': f'Assume you are an academic advisor. Based on this list of my interests ({interestList}, pick 15 classes from the list of potential classes ({self.courseData}) and explain why you have selected them. Match your selections as closely as possible to my interests. Make sure you pick exactly 15.)'}
        response_content = []
        print(message)

        for part in ollama.chat(model='llama3.2', messages=[message], stream=True):
            content = part['message']['content']
            print(content, end='', flush=True)
            response_content.append(content)

        print(''.join(response_content))
        return ''.join(response_content)

    #returns the matching interests from the interestIndicies list
    @staticmethod
    def matchInterests(user: dict) -> list:
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
        