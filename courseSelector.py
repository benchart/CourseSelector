import json
from chatbot.chatbotModel import ChatbotModel
from userManagement import UserManagement

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

    @staticmethod
    def findRelevantCourses(interestList: list):
        print()
        self.model.callChatbot
        #store class code in an array to be retrieved from later

    def findCourseByParameter(self, databasePath: str):
       for course in self.courseData:
           if(course['class_code'] == 'HHC-H 101'):
               print(course)
           
    
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
        