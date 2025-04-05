from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_view, name='chatbot'),  
    path("delete-account/", views.delete_account, name="delete_account"),
]
