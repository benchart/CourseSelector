from django.shortcuts import render
from .chatbotModel import ChatbotModel

def chatbot_view(request):
    response = None
    if request.method == "POST":
        user_input = request.POST.get("message")
        if user_input:
            model = ChatbotModel()
            response = model.does_not_match(user_input)  # or model.callChatbot(user_input) if fully functional

    return render(request, "chatbot.html", {"response": response})

