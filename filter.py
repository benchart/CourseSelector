from chatbotModel import ChatbotModel
from userManagement import UserManagement
from courseSelector import CourseSelector
import json

class Filter:
    courseModel = CourseSelector()
    courseModel.findCourseByParameter("courseDatabase.txt")

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