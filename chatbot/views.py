from django.utils.timezone import now
from django.shortcuts import render
from .chatbotModel import ChatbotModel

def chatbot_view(request):
    if "chat_history" not in request.session:
        request.session["chat_history"] = []

    # Clear chat if requested
    if request.method == "POST" and "clear" in request.POST:
        request.session["chat_history"] = []
        request.session.modified = True
        return render(request, "chatbot.html", {"chat_history": []})

    response = None
    user_input = None

    if request.method == "POST" and "message" in request.POST:
        user_input = request.POST.get("message")

        if user_input:
            model = ChatbotModel()
            response = model.does_not_match(user_input)

            # Add user + bot messages with timestamps
            request.session["chat_history"].append({
                "sender": "user",
                "message": user_input,
                "timestamp": now().strftime("%I:%M %p")
            })
            request.session["chat_history"].append({
                "sender": "bot",
                "message": response,
                "timestamp": now().strftime("%I:%M %p")
            })

            request.session.modified = True

    return render(request, "chatbot.html", {
        "chat_history": request.session.get("chat_history", [])
    })

# from django.shortcuts import render
# from .chatbotModel import ChatbotModel

# def chatbot_view(request):
#     if "chat_history" not in request.session:
#         request.session["chat_history"] = []

#     response = None
#     user_input = None

#     if request.method == "POST":
#         user_input = request.POST.get("message")

#         if user_input:
#             model = ChatbotModel()
#             response = model.does_not_match(user_input)

#             # Add user and bot messages to session
#             request.session["chat_history"].append({
#                 "sender": "user",
#                 "message": user_input
#             })
#             request.session["chat_history"].append({
#                 "sender": "bot",
#                 "message": response
#             })

#             request.session.modified = True

#     return render(request, "chatbot.html", {
#         "chat_history": request.session.get("chat_history", [])
#     })
