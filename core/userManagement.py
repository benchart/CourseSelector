import json
import numpy as np

class UserManagement:   
    studentFilepath = "studentData.txt"
    adminFilepath = "adminData.txt"

    def __init__(self, studentFilepath: str, adminFilepath: str):
        self.studentFilepath = studentFilepath
        self.adminFilepath = adminFilepath

    #reads through the file to prevent adding duplicates
    @staticmethod
    def determineDuplicate(filepath: str, search_string: dict) -> bool:
        try:
            with open(filepath, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    user_data = json.loads(line.strip())
                    user_name = json.loads(search_string.strip())  # Convert each line back into a dictionary
                    if user_data['username'].lower() == user_name['username'].lower():  # Compare by username
                        print("User already exists")
                        return False
                return True
        except FileNotFoundError:
            print(f"Error: File not found at {filepath}")
            return FileNotFoundError
    
    #creates a new user based on the specified parameters
    @staticmethod
    def createNewStudent(fullName: str, userName: str, age: int, classStanding: str, numCredits: int, interestIndicies: np.array):
        data = {
            "name": fullName,
            "username": userName,
            "age": age,
            "class": classStanding,
            "credits": numCredits,
            "interestIndicies": interestIndicies
        }

        newUser = json.dumps(data)

        #run the new user through the file to determine if it already exists
        if(UserManagement.determineDuplicate(UserManagement.studentFilepath, newUser)):
            try:
                with open(UserManagement.studentFilepath, "a") as file:
                    file.write((newUser) + "\n")
            except FileNotFoundError:
                print(F"Error: File not found at {UserManagement.studentFilepath}")
                return FileNotFoundError
            
    #creates a new user based on the specified parameters
    @staticmethod
    def createNewAdmin(fullName: str, userName: str, age: int, adminPasskey: int):
        data = {
            "name": fullName,
            "username": userName,
            "age": age,
            "admin key": adminPasskey
        }

        newUser = json.dumps(data)

        #run the new user through the file to determine if it already exists
        if(UserManagement.determineDuplicate(UserManagement.adminFilepath, newUser)):
            try:
                with open(UserManagement.adminFilepath, "a") as file:
                    file.write((newUser) + "\n")
            except FileNotFoundError:
                print(F"Error: File not found at {UserManagement.adminFilepath}")
                return FileNotFoundError
        
    #returns the json string containing the specified student's data
    @staticmethod
    def readStudent(username: str, studentPath: str) -> str:
        try:
            with open(studentPath, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    user_data = json.loads(line.strip())
                    if user_data['username'].lower() == username.lower():  # Compare by username
                        return line
                return "No matching user found"
        except FileNotFoundError:
            print(F"Error: File not found at {studentPath}")
            return FileNotFoundError

    #returns the json string containing the specified admin's data
    @staticmethod
    def readAdmin(username: str, adminPath: str) -> str:
        try:
            with open(adminPath, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    user_data = json.loads(line.strip())
                    if user_data['username'].lower() == username.lower():  # Compare by username
                        return line
                return "No matching user found"
        except FileNotFoundError:
            print(F"Error: File not found at {adminPath}")
            return FileNotFoundError

    #higher-up method for searching for users
    @staticmethod   
    def findUser(user: str, userType: bool) -> str:      
        """
        Finds a user in the database based on their username
        If the user is an admin, userType is true
        If the user is a student, userType is false

        Arguments:
            user: the username of the user in string notation
            userType: boolean value indicating which type of user you're looking for:
                    false = student
                    true = admin

        Returns:
            str: The json object associated with that user
        """
        if(userType):
            return UserManagement.readAdmin(user, UserManagement.adminFilepath)
        else: 
            return UserManagement.readStudent(user, UserManagement.studentFilepath)