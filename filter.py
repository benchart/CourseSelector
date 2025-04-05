from chatbotModel import ChatbotModel
from userManagement import UserManagement


# model = ChatbotModel()
# model.callChatbot("whats a funny joke mike")
# model.callChatbot("tell me another funny joke")
# model.callChatbot("hello george")
# model.callChatbot("please list out all of the class descriptions")

userSystem = UserManagement()
userSystem.createNewStudent("Parley Hartwell", "phartwell", 19, "Freshman", 18)
userSystem.createNewAdmin("Parley Hartwell", "phartwell", 19, 157686)
print(userSystem.findUser("phartwell", True))