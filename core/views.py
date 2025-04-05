from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import StudentSignupForm, AdminSignupForm, LoginForm
from students.models import StudentProfile

ADMIN_PASSKEY = "SuperSecretKey123"
INTEREST_OPTIONS = ["Math", "Science", "Art", "Programming", "Robotics", "Design", "History"]

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
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                form.add_error("username", "Username already taken")
            else:
                user = User.objects.create_user(username=username, password=form.cleaned_data['password'])
                StudentProfile.objects.create(user=user, grade=form.cleaned_data['grade'])
                request.session['pending_user'] = username
                return redirect("/select-interests")
    else:
        form = StudentSignupForm()
    return render(request, "core/signup_student.html", {"form": form})

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
                return redirect("/admin/class-db")
    else:
        form = AdminSignupForm()
    return render(request, "core/signup_admin.html", {"form": form})

def select_interests(request):
    username = request.session.get("pending_user")
    if not username:
        return redirect("/")
    user = User.objects.get(username=username)
    profile = StudentProfile.objects.get(user=user)
    if request.method == "POST":
        selected = request.POST.getlist("interests")
        if len(selected) < 3:
            return render(request, "core/interest_select.html", {"interests": INTEREST_OPTIONS, "error": "Select at least 3."})
        profile.interests = ",".join(selected)
        profile.save()
        login(request, user)
        return redirect("/chat")
    return render(request, "core/interest_select.html", {"interests": INTEREST_OPTIONS})
