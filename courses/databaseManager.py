import json

class DatabaseManager:
    courseData: list[dict]
    databasePath: str

    def __init__(self, databasePath: str):
        self.courseData = self.readCourseList(databasePath)
        self.databasePath = databasePath
    
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

    #searches for a course based on a query and filters the dictionary of available classes
    def searchCourse(self, query: str) -> list[dict]:    
        newCourseList = []

        for course in self.courseData:
            for key in course.keys():
                if query.lower() in str(course.get(key)).lower():
                    newCourseList.append(course)
                    break
        for course in newCourseList:
            DatabaseManager.printCourse(course)
        return newCourseList

    @staticmethod
    def printCourse(course: dict):
         for key in course.keys():
            if(course.get(key) == ""):
                print("N/A")
            else:
                print(course.get(key))
         print("\n")

DBManager = DatabaseManager("courseDatabase.txt")
#DBManager.printCourse({"class_code": "CHEM-68708", "subject": "Philosophy", "catalog_number": "213", "instructor": "Lee C", "name": "Art History in Philosophy", "topic": "Art History", "start_time": "15:00", "end_time": "16:00", "days": "TR", "prerequisites": "", "units": 4.0, "description": "A deep dive into art history as it relates to philosophy."})
DBManager.searchCourse("chem")