from django.utils.timezone import now
from django.shortcuts import render, redirect
from .chatbotModel import ChatbotModel
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
import os
import json

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


def delete_account(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            username = request.user.username
            request.user.delete()
            logout(request)

            # Also remove from studentData.txt
            filepath = os.path.join("core", "studentData.txt")
            if os.path.exists(filepath):
                with open(filepath, "r") as file:
                    lines = file.readlines()
                with open(filepath, "w") as file:
                    for line in lines:
                        try:
                            data = json.loads(line.strip())
                            if data.get("username").lower() != username.lower():
                                file.write(json.dumps(data) + "\n")
                        except json.JSONDecodeError:
                            continue
    return redirect("/")


def login_and_manage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        return redirect("chatbot:chatbot")  # Go to chatbot after logging in
    return redirect("chatbot:chatbot")
