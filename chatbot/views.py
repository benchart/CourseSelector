from django.shortcuts import render, redirect
from .chatbotModel import ChatbotModel
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
import os
import json
from datetime import datetime
import pytz

def chatbot_view(request):
    # Initialize session-based chat history if it doesn't exist
    
    if request.GET.get("clear") == "true":
        request.session["chat_history"] = []
        return redirect("chatbot:chatbot")
    
    if "chat_history" not in request.session:
        request.session["chat_history"] = []

    response = None
    user_input = None

    # Handle user input from chatbox
    if request.method == "POST" and "message" in request.POST:
        user_input = request.POST.get("message")

        if user_input:
            try:
                model = ChatbotModel()
                response = model.callChatbot(user_input)
            except Exception as e:
                response = "⚠️ Unable to connect to your local Ollama instance. Please ensure it's installed and running by executing <code>ollama run llama3.2</code> in your terminal."

            # Optional: precise Indiana timezone timestamp
            # timestamp = now().astimezone(timezone('America/Indiana/Indianapolis')).strftime("%I:%M %p")
            #timestamp = now().strftime("%I:%M %p")

            indiana_tz = pytz.timezone("America/Indiana/Indianapolis")
            timestamp = datetime.now(indiana_tz).strftime("%I:%M %p")

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
    logout(request)
    request.session.flush()  # ✅ Clears chat + all session data
    return redirect("home")

def login_and_manage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Clear old chat history when a user logs in
            request.session["chat_history"] = []

        return redirect("chatbot:chatbot")

    return redirect("chatbot:chatbot")
