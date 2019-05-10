from django.urls import path
from . import views

app_name = 'interview'
urlpatterns = [
	path('home/', views.home, name='home'),
	path('questions/<str:topic>/', views.Questions.as_view(), name = 'questions'),
	path('results/', views.Results.as_view(), name='total_results'),
	path('strategies/', views.Strategies.as_view(), name='strategies')
]