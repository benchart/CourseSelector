import json

class UserManagement:   

    #reads through the file to prevent adding duplicates
    @staticmethod
    def determineDuplicate(filepath: str, search_string: str) -> bool:
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
    def createNewStudent(fullName: str, userName: str, age: int, classStanding: str, numCredits: int):
        data = {
            "name": fullName,
            "username": userName,
            "age": age,
            "class": classStanding,
            "credits": numCredits 
        }

        newUser = json.dumps(data)

        #run the new user through the file to determine if it already exists
        if(UserManagement.determineDuplicate("studentData.txt", newUser)):
            try:
                with open("studentData.txt", "a") as file:
                    file.write((newUser) + "\n")
            except FileNotFoundError:
                print("Error: File not found at studentData.txt")
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
        if(UserManagement.determineDuplicate("adminData.txt", newUser)):
            try:
                with open("adminData.txt", "a") as file:
                    file.write((newUser) + "\n")
            except FileNotFoundError:
                print("Error: File not found at adminData.txt")
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