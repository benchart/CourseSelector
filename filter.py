from chatbotModel import ChatbotModel
from userManagement import UserManagement
import json


model = ChatbotModel()
# model.callChatbot("whats a funny joke mike")
# model.callChatbot("tell me another funny joke")
model.callChatbot("find the admin with the username phartwell")
# model.callChatbot("hello george")
# model.callChatbot("please list out all of the class descriptions")

userSystem = UserManagement("studentData.txt", "adminData.txt")
userSystem.createNewStudent("Parley Hartwell", "phartwell", 19, "Freshman", 18, [1,6,7,10,100,23])
userSystem.createNewAdmin("Parley Hartwell", "phartwell", 19, 157686)
print(userSystem.findUser("phartwell", False))
y = json.loads(userSystem.findUser("phartwell", False))
print(y['interestIndicies'])