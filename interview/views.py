#Each view lives at a URL, thus, if you want to access a vew, you have to say where it lives in the urls.py directory of the app
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic 
from .forms import  all_models, all_formsets


def home(request):
	return render(request, 'interview/home.html')


def results(request):
	return render(request, 'interview/results.html')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'interview/signup.html'


class Questions(generic.TemplateView):
	"""This view looks up a model using a URL supplied topic, then creates/posts
		a form to update the user information for that model"""
	def get(self, request, topic):
		formset = all_formsets[topic] # assigns formset factory for appriate model
		user_forms = formset(queryset=all_models[topic].objects.filter(user=request.user)) # prepopulates fields with existing database information
		return render(request, "interview/questions.html", {'user_forms': user_forms, 'topic': topic})

	def post(self, request, topic):
		formset = all_formsets[topic]
		form = formset(request.POST)
		if form.is_valid():
			modified_forms = form.save(commit=False) # lets us add current user to entry before savinfg
			for instance in modified_forms: # for loop to account for possibility of multiple forms submitted simultaneously (ex: flights)
				instance.user = request.user
				instance.save()
				print('forms are saved')
			return HttpResponseRedirect(request.META['HTTP_REFERER']) # redirects to page that user was on
		else:
			print('form is not valid')
			return HttpResponseRedirect(request.META['HTTP_REFERER'])	


class Results(generic.TemplateView):
	def get(request):
		# initialize total footprint
		# for each model, get all rows associated with current user
		# for each associated row, call the footprint method of that and add the result to the total footprint
		# send the total footprint to the template page
		total_footprint = 0
		for topic in all_models:
			for instances in all_models[topic].objects.filter(user=request.user):
				total_footprint += request.user.model.footprint
		return render(request, "interview/footprint_results.html", {'total_footprint': total_footprint})