from django.urls import path
from . import views

app_name = 'interview'
urlpatterns = [
	path('home/', views.home, name='home'),
	path('results/', views.results, name='results'),
	#path('formset_test/', views.formset_test, name='formset_test'),
	#path('questions/residence/', views.Residence.as_view(), name = 'survey'),
	path('questions/<str:subject>/', views.GeneralCase.as_view(), name = 'survey'),
	#path("profile/", views.profile, name = 'profile'),
	#path('navigation/', views.navigation, name = 'navigation'),
#	path('transportation_navigation/', views.transportation_navigation, name= 'transportation_navigation'),
#	path('transportation/', views.transportation, name = 'transportation'),
	#path('<str:subject>/sub_navigation', views.sub_navigation, name = 'sub_navigation'),
	#path('<str:subject>/<sub_survey>', views.sub_survey, name = 'sub_survey'),
]