import json
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
    courseData: dict

    def __init__(self, databasePath: str):
        self.courseData = self.readCourseList(databasePath)

    #finds relevant classes based on the interest list
    def findRelevantCoursesByInterest(self, interestList: list):
        for course in self.courseData:
            topicString = course['topic']
            descString = course['descString']
        #store class code in an array to be retrieved from later

    #parses json data to find classes which fit the specified parameters
    def findCourseByParameter(self, parameter: str):
       match parameter:
        case "credits":
            self.courseData = self.getByNumCredits(self, 2.0, 4.0)
            return self.courseData
        case 400:
            return "Bad Request"
        case 404:
            return "Not Found"
        case _:
             self.courseData = self.getByType(self, parameter)
             return self.courseData
    
    #fetches course based on a specified parameter
    def getByType(self, parameterName: str, codeList: list) -> dict:
        newCourseList = {}
        try:
            for course in self.courseData:
                for code in codeList:
                    if(course[parameterName] == code):
                        newCourseList.update(course)
                        print(course)
                        continue
            return newCourseList
        except KeyError:
            print(F"parameter not found: {KeyError}")

    #filters classes based on specified credits range:
    def getByNumCredits(self, creditsMin: float, creditsMax: float) -> dict:
        newCourseList = {}
        try:
            for course in self.courseData:
                if ((int(course['units'])) >= creditsMin and (int(course['units'])) <= creditsMax):
                    print(course)
                    newCourseList.update(course)
            return newCourseList
        except ValueError:
            print(F"Error occured: {ValueError}")


    #returns the matching interests from the interestIndicies list
    @staticmethod
    def matchInterests(user: dict) -> list:
        interestArray: list = []
        try:
            for index in user['interestIndicies']:
                interestArray.append(INTEREST_OPTIONS[int(index)])
            return interestArray
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
    # Example: Print the class names and instructors
                        # for course in newJson:
                        #     print(f"Class Name: {course['name']}, Instructor: {course['instructor']}")
                        return newJson
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON: {e}")
        except FileNotFoundError as e:
            print(f"Filepath not found for {databasePath}")
        