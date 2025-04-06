from django.utils.timezone import now
from django.shortcuts import render, redirect
from .chatbotModel import ChatbotModel
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
import os
import json
# Optional: use this if you want strict Indiana timezone
# from pytz import timezone


def chatbot_view(request):
    # Initialize session-based chat history if it doesn't exist
    if "chat_history" not in request.session:
        request.session["chat_history"] = []

    response = None
    user_input = None

    # Handle user input from chatbox
    if request.method == "POST" and "message" in request.POST:
        user_input = request.POST.get("message")

        if user_input:
            model = ChatbotModel()
            response = model.does_not_match(user_input)

            # Optional: precise Indiana timezone timestamp
            # timestamp = now().astimezone(timezone('America/Indiana/Indianapolis')).strftime("%I:%M %p")
            timestamp = now().strftime("%I:%M %p")

            request.session["chat_history"].append({
                "sender": "user",
                "message": user_input,
                "timestamp": timestamp
            })
            request.session["chat_history"].append({
                "sender": "bot",
                "message": response,
                "timestamp": timestamp
            })

            request.session.modified = True

    return render(request, "chatbot.html", {
        "chat_history": request.session.get("chat_history", [])
    })

def delete_account(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            username = request.user.username.lower()

            # Delete Django user
            request.user.delete()
            logout(request)

            # Remove from studentData.txt
            filepath = os.path.join("core", "studentData.txt")
            if os.path.exists(filepath):
                print("Deleting from studentData.txt...")
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        lines = file.readlines()

                    with open(filepath, "w", encoding="utf-8") as file:
                        for line in lines:
                            try:
                                data = json.loads(line.strip())
                                if data.get("username", "").lower() != username:
                                    file.write(json.dumps(data) + "\n")
                                else:
                                    print(f"Removed user: {data.get('username')}")
                            except json.JSONDecodeError:
                                print("Skipping invalid JSON line")
                                continue
                except Exception as e:
                    print(f"Error processing studentData.txt: {e}")
    return redirect("/")

def login_and_manage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        return redirect("chatbot:chatbot")
    return redirect("chatbot:chatbot")

# from django.utils.timezone import now
# from django.shortcuts import render, redirect
# from .chatbotModel import ChatbotModel
# from django.contrib.auth import logout, login, authenticate
# from django.contrib.auth.models import User
# import os
# import json

# def chatbot_view(request):
#     if "chat_history" not in request.session:
#         request.session["chat_history"] = []

#     # Clear chat if requested
#     if request.method == "POST" and "clear" in request.POST:
#         request.session["chat_history"] = []
#         request.session.modified = True
#         return render(request, "chatbot.html", {"chat_history": []})

#     response = None
#     user_input = None

#     if request.method == "POST" and "message" in request.POST:
#         user_input = request.POST.get("message")

#         if user_input:
#             model = ChatbotModel()
#             response = model.does_not_match(user_input)

#             # Add user + bot messages with timestamps
#             request.session["chat_history"].append({
#                 "sender": "user",
#                 "message": user_input,
#                 "timestamp": now().strftime("%I:%M %p")
#             })
#             request.session["chat_history"].append({
#                 "sender": "bot",
#                 "message": response,
#                 "timestamp": now().strftime("%I:%M %p")
#             })

#             request.session.modified = True

#     return render(request, "chatbot.html", {
#         "chat_history": request.session.get("chat_history", [])
#     })


# def delete_account(request):
#     if request.method == "POST":
#         if request.user.is_authenticated:
#             username = request.user.username.lower()  # normalize case

#             # Delete from Django User model
#             request.user.delete()
#             logout(request)

#             # Also remove from studentData.txt
#             filepath = os.path.join("core", "studentData.txt")
#             if os.path.exists(filepath):
#                 print("Deleting from studentData.txt...")  # Debug
#                 try:
#                     with open(filepath, "r", encoding="utf-8") as file:
#                         lines = file.readlines()

#                     with open(filepath, "w", encoding="utf-8") as file:
#                         for line in lines:
#                             try:
#                                 data = json.loads(line.strip())
#                                 if data.get("username", "").lower() != username:
#                                     file.write(json.dumps(data) + "\n")
#                                 else:
#                                     print(f"Removed user: {data.get('username')}")
#                             except json.JSONDecodeError:
#                                 print("Skipping invalid JSON line")
#                                 continue
#                 except Exception as e:
#                     print(f"Error processing studentData.txt: {e}")
#     return redirect("/")


# def login_and_manage(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#         return redirect("chatbot:chatbot")  # Go to chatbot after logging in
#     return redirect("chatbot:chatbot")
