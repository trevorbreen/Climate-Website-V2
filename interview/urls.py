from django.urls import path
from django.contrib import admin

from . import views
from django.contrib.auth import views as auth_views

app_name = 'interview'
urlpatterns = [
	path('', views.home, name='home'),
	path('results/', views.results, name='results'),
	path('provide_survey/', views.provide_survey, name='provide_survey'),
	path('household/', views.household, name = 'household'),
	path('transportation/', views.transportation, name = 'transportation'),
	path('food/', views.food, name = 'food'),
	path('personal_info/', views.personal_info, name = 'personal_info'),
]