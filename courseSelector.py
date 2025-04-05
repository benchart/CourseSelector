import json
from chatbotModel import ChatbotModel
from userManagement import UserManagement

class CourseSelector:

    model = ChatbotModel()
    userSystem = UserManagement("studentData.txt", "adminData.txt")
    coursePath: str

    def __init__ (self, coursePath: str):
        self.coursePath = coursePath

    def findRelevantCourses():
        print()

    def findCourseByParameter():
        print()
    
    def readCourseList(coursePath: str):
        try:
            with open(coursePath, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    print(line)
        except FileNotFoundError:
            print(f"Error: File not found at {coursePath}")
            return FileNotFoundError
