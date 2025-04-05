import json
import numpy as np

class UserManagement:
    studentFilepath = "core/studentData.txt"
    adminFilepath = "adminData.txt"

    def __init__(self, studentFilepath: str, adminFilepath: str):
        self.studentFilepath = studentFilepath
        self.adminFilepath = adminFilepath

    # Reads through the file to prevent adding duplicates
    @staticmethod
    def determineDuplicate(filepath: str, search_data: dict) -> bool:
        try:
            with open(filepath, 'r') as file:
                lines = file.readlines()
            for line in lines:
                user_data = json.loads(line.strip())
                if user_data['username'].lower() == search_data['username'].lower():
                    print("User already exists")
                    return False
            return True
        except FileNotFoundError:
            print(f"Error: File not found at {filepath}")
            return FileNotFoundError
    
    #creates a new user based on the specified parameters
    @staticmethod
    def createNewStudent(fullName: str, userName: str, age: int, classStanding: str, numCredits: int, interestIndicies):
        data = {
        "name": fullName,
        "username": userName,
        "age": age,
        "class": classStanding,
        "credits": numCredits,
        "interestIndicies": interestIndicies
    }

        if UserManagement.determineDuplicate(UserManagement.studentFilepath, data):
            try:
                with open(UserManagement.studentFilepath, "a") as file:
                    file.write(json.dumps(data) + "\n")
            except FileNotFoundError:
                print(f"Error: File not found at {UserManagement.studentFilepath}")
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

        if UserManagement.determineDuplicate(UserManagement.adminFilepath, data):
            try:
                with open(UserManagement.adminFilepath, "a") as file:
                    file.write(json.dumps(data) + "\n")
            except FileNotFoundError:
                print(f"Error: File not found at {UserManagement.adminFilepath}")
                return FileNotFoundError

    # Returns the JSON string containing the specified student's data
    @staticmethod
    def readStudent(username: str, studentPath: str) -> str:
        try:
            with open(studentPath, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    user_data = json.loads(line.strip())
                    if user_data['username'].lower() == username.lower():
                        return line
                return "No matching user found"
        except FileNotFoundError:
            print(f"Error: File not found at {studentPath}")
            return FileNotFoundError

    # Returns the JSON string containing the specified admin's data
    @staticmethod
    def readAdmin(username: str, adminPath: str) -> str:
        try:
            with open(adminPath, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    user_data = json.loads(line.strip())
                    if user_data['username'].lower() == username.lower():
                        return line
                return "No matching user found"
        except FileNotFoundError:
            print(f"Error: File not found at {adminPath}")
            return FileNotFoundError

    # Higher-up method for searching for users
    @staticmethod
    def findUser(user: str, userType: bool) -> str:
        """
        Finds a user in the database based on their username.
        If the user is an admin, userType is True.
        If the user is a student, userType is False.

        Arguments:
            user: the username of the user in string format
            userType: boolean indicating type of user (False = student, True = admin)

        Returns:
            str: The JSON object associated with that user
        """
        if userType:
            return UserManagement.readAdmin(user, UserManagement.adminFilepath)
        else:
            return UserManagement.readStudent(user, UserManagement.studentFilepath)
