from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import StudentSignupForm, AdminSignupForm, LoginForm
from .userManagement import UserManagement  # <- Custom class
import json

ADMIN_PASSKEY = "SuperSecretKey123"
INTEREST_OPTIONS = [
    "Math", "Creative Writing", "Biology", "Robotics", "Music Theory",
    "World History", "Computer Programming", "Environmental Science", "Public Speaking",
    "Theater Arts", "Astronomy", "Psychology", "Film Studies", "Chemistry",
    "Political Science", "Entrepreneurship", "Photography", "Philosophy", "Statistics",
    "Debate", "Forensic Science", "Sociology", "Graphic Design", "Economics",
    "Physics", "Marine Biology", "UX Design", "Digital Media", "AI",
    "Game Development", "Ethics", "Anthropology", "Web Development", "Linguistics",
    "Cognitive Science", "Marketing", "Botany", "Data Science", "Education Policy",
    "Foreign Languages", "Geology", "Journalism", "Music Performance", "Gender Studies",
    "Classical Studies", "Animation", "Social Work", "Nanotech", "Zoology"
]

def home(request):
    return render(request, 'core/home.html')

def login_student(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect("/chat")
    else:
        form = LoginForm()
    return render(request, "core/login_student.html", {"form": form})

def login_admin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        access_key = request.POST.get("access_key")
        if form.is_valid() and access_key == ADMIN_PASSKEY:
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect("/admin/class-db")
        elif access_key != ADMIN_PASSKEY:
            form.add_error(None, "Invalid access key.")
    else:
        form = LoginForm()
    return render(request, "core/login_admin.html", {"form": form})

def signup_student(request):
    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        age = int(request.POST.get("age"))
        grade = request.POST.get("grade")
        credits = int(request.POST.get("credits"))

        if User.objects.filter(username=username).exists():
            return render(request, "core/signup_student.html", {
                "error": "Username already taken"
            })

        User.objects.create_user(username=username, password=password)

        # Save to studentData.txt
        UserManagement.createNewStudent(
            fullName=name,
            userName=username,
            age=age,
            classStanding=grade,
            numCredits=credits,
            interestIndicies=[]
        )

        request.session['pending_user'] = username
        return redirect("/select-interests")

    return render(request, "core/signup_student.html")

def signup_admin(request):
    if request.method == "POST":
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['passkey'] != ADMIN_PASSKEY:
                form.add_error("passkey", "Incorrect admin passkey")
            elif User.objects.filter(username=form.cleaned_data['username']).exists():
                form.add_error("username", "Username already taken")
            else:
                User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                UserManagement.createNewAdmin(
                    fullName=form.cleaned_data['username'],
                    userName=form.cleaned_data['username'],
                    age=21,
                    adminPasskey=ADMIN_PASSKEY
                )
                return redirect("/admin/class-db")
    else:
        form = AdminSignupForm()
    return render(request, "core/signup_admin.html", {"form": form})

def select_interests(request):
    if request.method == "POST":
        indices = request.POST.get("interests", "")
        index_list = indices.split(",") if indices else []

        if len(index_list) < 3:
            return render(request, "core/interest_select.html", {
                "interests": INTEREST_OPTIONS,
                "error": "Please select at least 3 interests."
            })

        selected_indices = [int(i) for i in index_list if i.isdigit()]
        selected_names = [INTEREST_OPTIONS[i] for i in selected_indices if i < len(INTEREST_OPTIONS)]
        username = request.session.get("pending_user")

        if username:
            # Update Django StudentProfile
            try:
                user = User.objects.get(username=username)
                profile = StudentProfile.objects.get(user=user)
                profile.interests = ",".join(selected_names)
                profile.save()
            except Exception as e:
                print("Could not update StudentProfile:", e)

            # Update studentData.txt
            try:
                filepath = UserManagement.studentFilepath
                with open(filepath, 'r') as f:
                    users = [json.loads(line.strip()) for line in f]

                for user in users:
                    if user["username"].lower() == username.lower():
                        user["interestIndicies"] = selected_indices
                        break

                with open(filepath, 'w') as f:
                    for user in users:
                        f.write(json.dumps(user) + "\n")

            except Exception as e:
                print("Error updating studentData.txt:", e)

        return redirect("/chat")

    return render(request, "core/interest_select.html", {"interests": INTEREST_OPTIONS})
