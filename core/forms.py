from django import forms
from django.contrib.auth.models import User

class StudentSignupForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    grade = forms.IntegerField(min_value=1, max_value=12)

class AdminSignupForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    passkey = forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class CourseForm(forms.Form):
    class_code = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=100)
    catalog_number = forms.CharField(max_length=20)
    instructor = forms.CharField(max_length=100)
    name = forms.CharField(max_length=200)  # ⬅️ was small
    topic = forms.CharField(max_length=100)
    start_time = forms.CharField(max_length=20)
    end_time = forms.CharField(max_length=20)
    days = forms.CharField(max_length=50)  # ⬅️ increased
    prerequisites = forms.CharField(max_length=300, required=False)  # ⬅️ increased
    units = forms.FloatField()
    description = forms.CharField(widget=forms.Textarea, required=False)