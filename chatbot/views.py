from django.shortcuts import render
from .chatbotModel import ChatbotModel

def chatbot_view(request):
    if "chat_history" not in request.session:
        request.session["chat_history"] = []

    response = None
    user_input = None

    if request.method == "POST":
        user_input = request.POST.get("message")

        if user_input:
            model = ChatbotModel()
            response = model.does_not_match(user_input)

            # Add user and bot messages to session
            request.session["chat_history"].append({
                "sender": "user",
                "message": user_input
            })
            request.session["chat_history"].append({
                "sender": "bot",
                "message": response
            })

            request.session.modified = True

    return render(request, "chatbot.html", {
        "chat_history": request.session.get("chat_history", [])
    })



# from django.shortcuts import render
# from .chatbotModel import ChatbotModel

# def chatbot_view(request):
#     response = None
#     if request.method == "POST":
#         user_input = request.POST.get("message")
#         if user_input:
#             model = ChatbotModel()
#             response = model.does_not_match(user_input)  # or model.callChatbot(user_input) if fully functional

#     return render(request, "chatbot.html", {"response": response})

