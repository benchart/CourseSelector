import json
from chatbotModel import ChatbotModel
from userManagement import UserManagement
from course_dataset import course_dataset

class CourseSelector:

    model = ChatbotModel()
    userSystem = UserManagement("studentData.txt", "adminData.txt")

    def findRelevantCourses():
        print()

    @staticmethod
    def findCourseByParameter(databasePath: str):
        try:
            with open(databasePath, "r") as file:
                    json_data = file.readline()
                    try:
                        newJson = json.loads(json_data)
    # Example: Print the class names and instructors
                        for course in newJson:
                            print(f"Class Name: {course['name']}, Instructor: {course['instructor']}")
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON: {e}")
        except FileNotFoundError as e:
            print(f"Filepath not found for {databasePath}")
    
    def readCourseList(coursePath: str):
        try:
            with open(coursePath, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    print(line)
        except FileNotFoundError:
            print(f"Error: File not found at {coursePath}")
            return FileNotFoundError
