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
    class_code = forms.CharField(label="Class Code", max_length=20)
    subject = forms.CharField(label="Subject", max_length=100)
    catalog_number = forms.IntegerField(label="Catalog Number")
    instructor = forms.CharField(label="Instructor", max_length=100)
    name = forms.CharField(label="Course Title", max_length=200)
    topic = forms.CharField(label="Topic", max_length=200, required=False)
    start_time = forms.CharField(label="Start Time", max_length=10)
    end_time = forms.CharField(label="End Time", max_length=10)
    days = forms.CharField(label="Days", max_length=20)
    prereqs = forms.CharField(label="Prerequisites", max_length=200, required=False)
    units = forms.FloatField(label="Units")
    description = forms.CharField(label="Description", widget=forms.Textarea)