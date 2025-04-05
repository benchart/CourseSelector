from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/student/', views.login_student, name='login_student'),
    path('login/admin/', views.login_admin, name='login_admin'),
    path('signup/student/', views.signup_student, name='signup_student'),
    path('signup/admin/', views.signup_admin, name='signup_admin'),
    path('select-interests/', views.select_interests, name='select_interests'),
]
