import json

class UserManagement:
    studentFilepath = "core/studentData.txt"
    adminFilepath = "core/adminData.txt"

    def __init__(self, studentFilepath: str, adminFilepath: str):
        self.studentFilepath = studentFilepath
        self.adminFilepath = adminFilepath

    # Reads through the file to prevent adding duplicates
    @staticmethod
    def _determineDuplicate(filepath: str, search_data: dict) -> bool:
        try:
            with open(filepath, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        user_data = json.loads(line)
                    except json.JSONDecodeError:
                        print(f"Skipping invalid JSON line: {line}")
                        continue
                    if user_data['username'].lower() == search_data['username'].lower():
                        print("User already exists")
                        return False
            return True
        except FileNotFoundError:
            print(f"Error: File not found at {filepath}")
            return FileNotFoundError

    # Creates a new student
    @staticmethod
    def createNewStudent(fullName: str, userName: str, password: str, age: int, classStanding: str, numCredits: int, interestIndicies):
        data = {
            "name": fullName,
            "username": userName,
            "password": password,
            "age": age,
            "class": classStanding,
            "credits": numCredits,
            "interestIndicies": interestIndicies
        }

        if UserManagement._determineDuplicate(UserManagement.studentFilepath, data):
            try:
                with open(UserManagement.studentFilepath, "a") as file:
                    file.write(json.dumps(data) + "\n")
            except FileNotFoundError:
                print(f"Error: File not found at {UserManagement.studentFilepath}")
                return FileNotFoundError

    # ✅ Fixed indentation for createNewAdmin
    @staticmethod
    def createNewAdmin(userName: str, password: str, adminPasskey: str):
        data = {
            "username": userName,
            "password": password,
            "admin key": adminPasskey
        }

        if UserManagement._determineDuplicate(UserManagement.adminFilepath, data):
            try:
                with open(UserManagement.adminFilepath, "a") as file:
                    file.write(json.dumps(data) + "\n")
            except FileNotFoundError:
                print(f"Error: File not found at {UserManagement.adminFilepath}")
                return FileNotFoundError

    # Returns a student JSON string
    @staticmethod
    def _readStudent(username: str, studentPath: str) -> dict:
        try:
            with open(studentPath, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        user_data = json.loads(line)
                        if user_data['username'].lower() == username.lower():
                            return user_data
                    except json.JSONDecodeError:
                        continue
            return "No matching user found"
        except FileNotFoundError:
            print(f"Error: File not found at {studentPath}")
            return FileNotFoundError

    # Returns an admin JSON string
    @staticmethod
    def _readAdmin(username: str, adminPath: str) -> dict:
        try:
            with open(adminPath, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        user_data = json.loads(line)
                        if user_data['username'].lower() == username.lower():
                            return user_data
                    except json.JSONDecodeError:
                        continue
            return "No matching user found"
        except FileNotFoundError:
            print(f"Error: File not found at {adminPath}")
            return FileNotFoundError

    # General method to find a user
    @staticmethod
    def findUser(user: str, userType: bool) -> dict:
        if userType:
            return UserManagement._readAdmin(user, UserManagement.adminFilepath)
        else:
            return UserManagement._readStudent(user, UserManagement.studentFilepath)
