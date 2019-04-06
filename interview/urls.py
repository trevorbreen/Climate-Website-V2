from django.urls import path
from . import views

app_name = 'interview'
urlpatterns = [
	path('home/', views.home, name='home'),
	path('results/', views.Results.as_view(), name='results'),
	path('questions/<str:topic>/', views.Questions.as_view(), name = 'questions'),
]