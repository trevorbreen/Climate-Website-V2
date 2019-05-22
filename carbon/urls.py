"""carbon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from interview import views as int_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('interview/', include('interview.urls')),
	path('logout/', auth_views.LogoutView.as_view(template_name = 'interview/logged_out.html', next_page = '/login/'), name = 'logout'),
	path('login/', auth_views.LoginView.as_view(template_name ='interview/login.html'), name = 'login'),
	path('signup/', int_views.SignUp.as_view(), name = 'signup'),
	path('', include('django.contrib.auth.urls')),
    path('', int_views.splash, name = 'splash'),
]
