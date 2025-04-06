from django.urls import path
from . import views

app_name = 'chatbot'  # Enables namespacing

urlpatterns = [
    path('', views.chatbot_view, name='chatbot'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('login-and-manage/', views.login_and_manage, name='login_and_manage'),
    path('logout/', views.logout_view, name='logout'),
]
