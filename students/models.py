# This file defines the StudentProfile model, which extends the User model to include additional fields specific to students.
# It includes fields for grade, interests, and classes taken. The model uses a one-to-one relationship with the User model to ensure that each student has a unique profile.
from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.PositiveIntegerField()
    interests = models.TextField(blank=True, help_text="Comma-separated interests")
    classes_taken = models.TextField(blank=True, help_text="Comma-separated class codes")

    def __str__(self):
        return self.user.username
