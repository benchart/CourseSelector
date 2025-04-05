import json

class UserManagement:   

    #reads through the file to prevent adding duplicates
    @staticmethod
    def process_file(filepath: str, search_string: str) -> bool:
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
        if(UserManagement.process_file("studentData.txt", newUser)):
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
        if(UserManagement.process_file("adminData.txt", newUser)):
            try:
                with open("adminData.txt", "a") as file:
                    file.write((newUser) + "\n")
            except FileNotFoundError:
                print("Error: File not found at adminData.txt")
                return FileNotFoundError