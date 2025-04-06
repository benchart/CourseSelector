from chatbot.chatbotModel import ChatbotModel
from core.userManagement import UserManagement
from courseSelector import CourseSelector

class Filter:
    courseModel = CourseSelector("courseDatabase.txt")
    #courseModel.findCourseByParameter("courseDatabase.txt")
    #courseModel.getByClassCode(["PHIL-51184", "HON-41049"])
    #courseModel.getByType("name", ["Art History in Biology", "Opera in Biology"])
    courseModel.filterClassesMaster(
        catalogueNumMax='', 
        catalogueNumMin='', 
        class_code=[], 
        creditMax='', 
        creditMin=0, 
        instructorName=[], 
        status=False, 
        subjectName=[], 
        username=''
    )

    
    model = ChatbotModel()
    #model.callChatbot("whats a funny joke mike")
# model.callChatbot("tell me another funny joke")
#model.callChatbot("please tell me the descriptions of all of the courses")
# model.callChatbot("hello george")
    #model.callChatbot("what classes should I take if I don't want any morning classes")

    userSystem = UserManagement("studentData.txt", "adminData.txt")
    # userSystem.createNewStudent("Parley Hartwell", "phartwell", 19, "Freshman", 18, [1,6,7,10,100,23])
    # userSystem.createNewAdmin("Parley Hartwell", "phartwell", 19, 157686)
    #print(userSystem.findUser("phartwell", False))
    #y = json.loads(userSystem.findUser("phartwell", False))
    #print(courseModel.matchInterests(y))
    #print("\n\n\n\n")
    #courseModel.findRelevantCoursesByInterest("phartwell", False)