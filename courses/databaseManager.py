import json

class DatabaseManager:

    courseData: list[dict]
    databasePath: str

    def __init__(self, databasePath: str):
        self.courseData = self.readCourseList(databasePath)
        self.databasePath = databasePath
    
    
    #database functionality

    #adds a new course to the database via the specified parameters
    def addNewCourse(self, class_code: str, subject: str,
                     catalog_number: int, instructor: str,
                     name: str, topic: str,
                     start_time: str, end_time: str,
                     days: str, prereqs: str,
                     units: float, description: str):
        
        newCourse = DatabaseManager.updateCourse(class_code, subject, catalog_number, instructor, name, topic, start_time, end_time, days, prereqs, units, description)
        self.courseData = self.readCourseList(self.databasePath)
        self.courseData.append(newCourse)

        self.writeCourseList(self.databasePath)

    #returns a new course dictionary with the specified parameters
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
    def readCourseList(databasePath: str) -> list:
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