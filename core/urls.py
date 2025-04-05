from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/<str:user_type>', views.login_view, name='login'),
    path('signup/student', views.signup_student, name='signup_student'),
    path('signup/admin', views.signup_admin, name='signup_admin'),
    path('select-interests', views.select_interests, name='select_interests'),
    path("select-interests/", views.select_interests, name="select_interests"),
]