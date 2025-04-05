"""
URL configuration for smart_course_selector project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),                    # Django's default admin panel
    path('', include('core.urls')),                     # Your main app (home, login, etc.)
    path('students/', include('students.urls')),        # Student-specific routes
    path('admins/', include('admins.urls')),            # Admin account management
    path('courses/', include('courses.urls')),          # Courses
    path("chat/", include("chatbot.urls", namespace="chatbot")),             # ✅ Your chatbot app!
]

