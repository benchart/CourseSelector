from chatbotModel import ChatbotModel
from userManagement import UserManagement


model = ChatbotModel()
model.callChatbot("whats a funny joke mike")
model.callChatbot("tell me another funny joke")
model.callChatbot("hello george")
model.callChatbot("please list out all of the class descriptions")

userSystem = UserManagement()
userSystem.createNewUser("Parley Hartwell", "phartwell", 19, "Freshman", 18)