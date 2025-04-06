import json

class DatabaseManager:
    courseData: list[dict]
    databasePath: str

    def __init__(self, databasePath: str):
        self.courseData = self.readCourseList(databasePath)
        self.databasePath = databasePath
    
    
    #database functionality
    @staticmethod
    def updateCourse(class_code: str, subject: str,
                     catalog_number: int, instructor: str,
                     name: str, topic: str,
                     start_time: str, end_time: str,
                     days: str, prereqs: str,
                     units: float, description: str) -> dict:
        newCourse = {}
        newCourse.update({'class_code': class_code, 'subject': subject, 
                          'catalog_number': catalog_number, 'instructor': instructor,
                          'name': name, 'topic': topic,
                          'start_time': start_time, 'end_time': end_time,
                          'days': days, 'prerequisites': prereqs,
                          'units': units, 'description': description}
                          )
        return newCourse

    #allows the admin to edit a course's data within the database
    def editCourseData(self, prevCourse: dict, newCourse: dict):
        #reloads the courseData from the database file before writing to it
        self.courseData = self.readCourseList(self.databasePath)

        courseIndex = self.getIndexOfCourse(prevCourse)

        if courseIndex != -1:
            self.courseData[courseIndex] = newCourse
            self.writeCourseList(self.databasePath)
        else:
            print("Course not Found")
        

    #returns the index of the course found in the courseData list[dict]
    def getIndexOfCourse(self, searchCourse: dict) -> int:
        for index, baseCourse in enumerate(self.courseData):
            if baseCourse == searchCourse:
                return index
        return -1
    
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

    #prints out a course in a readable format
    @staticmethod
    def printCourse(course: dict):
         for key in course.keys():
            if(course.get(key) == ""):
                print("N/A")
            else:
                print(course.get(key))
         print("\n")



    #manage the database
    
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
    
    #write updated course data to the main database.txt
    def writeCourseList(self, databasePath: str):
        try:
            with open(databasePath, "w") as file:
                    file.write(json.dumps(self.courseData))
        except FileNotFoundError:
            print(f"Error: File not found at {databasePath}")
            return FileNotFoundError
        


DBManager = DatabaseManager("courseDatabase.txt")
y = DBManager.updateCourse("HHC-H 105","Education","101","Drake J","Education and Its Aims","General Education Foundations","09:45","11:00","M", "",1.5,"Required of all new Hutton students pursuing HHN as of Fall 2024.")
DBManager.editCourseData({"class_code": "CHEM-68708", "subject": "Philosophy", "catalog_number": "213", "instructor": "Lee C", "name": "Art History in Philosophy", "topic": "Art History", "start_time": "15:00", "end_time": "16:00", "days": "TR", "prerequisites": "", "units": 4.0, "description": "A deep dive into art history as it relates to philosophy."}, y)
#DBManager.searchCourse("chem")
for course in DBManager.courseData:
    DBManager.printCourse(course)