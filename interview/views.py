#Each view lives at a URL, thus, if you want to access a vew, you have to say where it lives in the urls.py directory of the app
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Survey
from .forms import SurveyForm

# link to pages
#def interview(request):
#	return render(request, 'interview/interview.html')
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'interview/signup.html'

def home(request):
	return render(request, 'interview/home.html')

def results(request):
	return render(request, 'interview/results.html')

def household(request):
	return render(request, 'interview/household.html')

def transportation(request):
	return render(request, 'interview/transportation.html')

def food(request):
	return render(request, 'interview/food.html')

def personal_info(request):
	return render(request, 'interview/personal_info.html')


#Get Survey and Save results
def provide_survey(request):
	if request.method == 'POST':
		form = SurveyForm(request.POST)
		print("Post requst")
		if form.is_valid():
			print('form is valid')
			print(request.user)
			modified_form = form.save(commit=False)
			modified_form.user = request.user
			modified_form.save()
			print('form is saved')
			return HttpResponseRedirect('../results')
		else:
			print('form is not valid')
			render(request, 'interview/interview.html')
	else:
		print("get empty form")
		form = SurveyForm()
	return render(request, 'interview/interview.html', {'form': form})

# class based views 
# Postgresql for database - get familiar with writing queries get things out and put them back in
#ERD diagrams (entity relation diagrams can help plan a database)
#Effient way to get a many to many mapping is a lookup table