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
    def findCourseByParameter():
        newUser = json.dumps(course_dataset)
        for course in newUser:
            print(f"Class Name: {course['name']}, Instructor: {course['instructor']}")

        #run the new user through the file to determine if it already exists
        try:
            with open("courseDatabase.txt", "a") as file:
                    file.write((newUser) + "\n")
        except FileNotFoundError:
            print(F"Error: File not found at courseDatabase.txt")
            return FileNotFoundError

    
    def readCourseList(coursePath: str):
        try:
            with open(coursePath, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    print(line)
        except FileNotFoundError:
            print(f"Error: File not found at {coursePath}")
            return FileNotFoundError
