from chatbotModel import ChatbotModel
from userManagement import UserManagement
from courseSelector import CourseSelector
import json

courseModel = CourseSelector()
#courseModel.findCourseByParameter()

model = ChatbotModel()
# model.callChatbot("whats a funny joke mike")
# model.callChatbot("tell me another funny joke")
#model.callChatbot("please tell me the descriptions of all of the courses")
# model.callChatbot("hello george")
# model.callChatbot("please list out all of the class descriptions")

userSystem = UserManagement("studentData.txt", "adminData.txt")
userSystem.createNewStudent("Parley Hartwell", "phartwell", 19, "Freshman", 18, [1,6,7,10,100,23])
userSystem.createNewAdmin("Parley Hartwell", "phartwell", 19, 157686)
print(userSystem.findUser("phartwell", False))
y = json.loads(userSystem.findUser("phartwell", False))
print(y['interestIndicies'])

# Assuming the provided JSON data is saved as a string
json_data = '''[
    {"class_code": "HHC-H 101", "subject": "Education", "catalog_number": "101", "instructor": "Drake J", "name": "Education and Its Aims", "topic": "General Education Foundations", "start_time": "09:45", "end_time": "11:00", "days": "M", "prerequisites": "", "units": 1.5, "description": "Required of all new Hutton students pursuing HHN as of Fall 2024."},
    {"class_code": "HON-H 228", "subject": "Colloquia", "catalog_number": "228", "instructor": "Evans G", "name": "Modern Madness", "topic": "Interdepartmental Colloquia", "start_time": "11:30", "end_time": "12:45", "days": "TR", "prerequisites": "", "units": 3.0, "description": "Explores themes of madness across disciplines."},
    {"class_code": "HON-H 240", "subject": "Science & Society", "catalog_number": "240", "instructor": "Winston W", "name": "Analytics, Sports & Winning Edge", "topic": "Sports Analytics", "start_time": "15:00", "end_time": "16:15", "days": "MW", "prerequisites": "", "units": 3.0, "description": "Examines competitive advantage through analytics in sports."},
    {"class_code": "CSCI-H 211", "subject": "Computer Science", "catalog_number": "211", "instructor": "Unknown", "name": "Intro to Computer Science - Honors", "topic": "Computer Science Fundamentals", "start_time": "TBD", "end_time": "TBD", "days": "TBD", "prerequisites": "", "units": 4.0, "description": "Introduction to computer science with an honors curriculum."},
    {"class_code": "SLAV-T 230", "subject": "Slavic Studies", "catalog_number": "230", "instructor": "Unknown", "name": "Vampires", "topic": "Cultural Studies", "start_time": "TBD", "end_time": "TBD", "days": "TBD", "prerequisites": "", "units": 3.0, "description": "Explores the image of vampires in European and American cultures."},
    {"class_code": "CSCI-96525", "subject": "History", "catalog_number": "394", "instructor": "Chen F", "name": "Feminist Theory in History", "topic": "Feminist Theory", "start_time": "13:00", "end_time": "14:00", "days": "TR", "prerequisites": "", "units": 3.0, "description": "A deep dive into feminist theory as it relates to history."},
    {"class_code": "HON-29728", "subject": "History", "catalog_number": "404", "instructor": "Lee C", "name": "Feminist Theory in History", "topic": "Feminist Theory", "start_time": "9:00", "end_time": "10:00", "days": "T", "prerequisites": "", "units": 1.0, "description": "A deep dive into feminist theory as it relates to history."},
    {"class_code": "CHEM-87113", "subject": "Biology", "catalog_number": "347", "instructor": "Nguyen G", "name": "Feminist Theory in Biology", "topic": "Feminist Theory", "start_time": "10:00", "end_time": "11:00", "days": "T", "prerequisites": "", "units": 3.0, "description": "A deep dive into feminist theory as it relates to biology."},
    {"class_code": "HHC-52001", "subject": "Biology", "catalog_number": "260", "instructor": "Patel E", "name": "Cultural Anthropology in Biology", "topic": "Cultural Anthropology", "start_time": "13:00", "end_time": "14:00", "days": "TR", "prerequisites": "", "units": 3.0, "description": "A deep dive into cultural anthropology as it relates to biology."},
    {"class_code": "PHIL-38258", "subject": "History", "catalog_number": "319", "instructor": "Kim D", "name": "Genetics in History", "topic": "Genetics", "start_time": "14:00", "end_time": "15:00", "days": "MW", "prerequisites": "", "units": 1.0, "description": "A deep dive into genetics as it relates to history."},
    {"class_code": "CHEM-62148", "subject": "Linguistics", "catalog_number": "311", "instructor": "Kim D", "name": "Logic in Linguistics", "topic": "Logic", "start_time": "13:00", "end_time": "14:00", "days": "MW", "prerequisites": "", "units": 2.0, "description": "A deep dive into logic as it relates to linguistics."},
    {"class_code": "MATH-76439", "subject": "Music", "catalog_number": "350", "instructor": "Lee C", "name": "Genetics in Music", "topic": "Genetics", "start_time": "10:00", "end_time": "11:00", "days": "R", "prerequisites": "", "units": 3.0, "description": "A deep dive into genetics as it relates to music."},
    {"class_code": "ART-23510", "subject": "Theater", "catalog_number": "412", "instructor": "Brown H", "name": "Ethics in Theater", "topic": "Ethics", "start_time": "9:00", "end_time": "10:00", "days": "T", "prerequisites": "", "units": 3.0, "description": "A deep dive into ethics as it relates to theater."},
    {"class_code": "ART-62137", "subject": "History", "catalog_number": "396", "instructor": "Patel E", "name": "Thermodynamics in History", "topic": "Thermodynamics", "start_time": "14:00", "end_time": "15:00", "days": "TR", "prerequisites": "", "units": 3.0, "description": "A deep dive into thermodynamics as it relates to history."},
    {"class_code": "CHEM-24481", "subject": "Physics", "catalog_number": "406", "instructor": "Nguyen G", "name": "Thermodynamics in Physics", "topic": "Thermodynamics", "start_time": "14:00", "end_time": "15:00", "days": "T", "prerequisites": "", "units": 2.0, "description": "A deep dive into thermodynamics as it relates to physics."},
    {"class_code": "CHEM-35439", "subject": "Biology", "catalog_number": "140", "instructor": "Chen F", "name": "Art History in Biology", "topic": "Art History", "start_time": "15:00", "end_time": "16:00", "days": "R", "prerequisites": "", "units": 1.0, "description": "A deep dive into art history as it relates to biology."},
    {"class_code": "PHIL-96454", "subject": "Physics", "catalog_number": "437", "instructor": "Patel E", "name": "Thermodynamics in Physics", "topic": "Thermodynamics", "start_time": "8:00", "end_time": "9:00", "days": "T", "prerequisites": "", "units": 2.0, "description": "A deep dive into thermodynamics as it relates to physics."},
    {"class_code": "HHC-97406", "subject": "Biology", "catalog_number": "114", "instructor": "Brown H", "name": "Opera in Biology", "topic": "Opera", "start_time": "9:00", "end_time": "10:00", "days": "R", "prerequisites": "", "units": 4.0, "description": "A deep dive into opera as it relates to biology."}
]'''


# Parse the JSON string into a Python object
data = json.loads(json_data)

# Example: Print the class names and instructors
for course in data:
    print(f"Class Name: {course['name']}, Instructor: {course['instructor']}")
