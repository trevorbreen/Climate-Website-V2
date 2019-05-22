from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic 
from .forms import  CustomUserCreationForm, all_models, all_formsets
from .parameters import carbon_footprint
#from .strategies import *


def return_user_data_instance(request, django_model_string, index=0, return_all_instances=False):
	if return_all_instances:
		return all_models[django_model_string].objects.filter(user=request.user)
	else:
		return all_models[django_model_string].objects.filter(user=request.user)[index]

def splash(request):
	return render(request, 'interview/splash.html')


def home(request):
	return render(request, 'interview/home.html')


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'interview/signup.html'


class Questions(generic.TemplateView):
	"""This view looks up a model using a URL supplied topic, then creates
		a form to update the user information for that model"""
	def get(self, request, topic):
		formset = all_formsets[topic] # creates expanding number of form copies for appropriate model
		user_forms = formset(queryset=all_models[topic].objects.filter(user=request.user)) # prepopulates fields with existing database information
		return render(request, "interview/questions.html", {'user_forms': user_forms, 'topic': topic})

	def post(self, request, topic):
		formset = all_formsets[topic]
		form = formset(request.POST)
		print(form)
		if form.is_valid():
			print('form is valid')
			modified_forms = form.save(commit=False) # lets us add current user to entry before saving three lines down
			print(modified_forms)
			for instance in modified_forms: # for loop to account for possibility of multiple forms submitted simultaneously (ex: flights)
				instance.user = request.user
				instance.save()
			return HttpResponseRedirect(request.META['HTTP_REFERER']) # valid form is saved and user redirected to same page
		else:
			print('form is not valid')
			return HttpResponseRedirect(request.META['HTTP_REFERER'])	# form is not valid


class Results(generic.TemplateView):
	"""For each item that the user described in their interview, send that item and it's footprint to the page and sum up a total footprint"""
	def get(self, request):
		context, footprint_table  = ({}, {'total itemized footprint': 0,}) # footprint_table must eventually be a value in the context dict so the template can loop over it
		for topic in all_models: # Loop through all item types (flights, electricity use, etc.)
			for index, item in enumerate(all_models[topic].objects.filter(user=request.user)): # Loop through each item of that type (car a, car b, etc.) 
				print(item)
				if topic == 'profile':
					footprint_table['income_estimate_footprint'] = item.footprint() # Seperated to allow for nonstandard naming
				else:
					footprint_table['total itemized footprint'] += float(item.footprint())
					footprint_table[str(topic)+str(index)] = item.footprint()
		context['footprint_table'] = footprint_table #see first line 
		return render(request, "interview/results.html", context)


def increase_fuel_efficiency(yearly_distance_driven, fuel_type, old_litres_per_hundred_km, new_litres_per_hundred_km):
	increase_in_efficiency_per_km = (old_litres_per_hundred_km - new_litres_per_hundred_km) * 100
	return increase_in_efficiency_per_km * carbon_footprint[fuel_type] *  yearly_distance_driven  

class Strategies(generic.TemplateView):
	def get(self, request):
		context, strategy_table  = ({}, {}) # footprint_table must eventually be a value in the context dict so the template can loop 
		electricity = return_user_data_instance(request, 'electricity')
		strategy_table['reduce electricity consumption by 10%' ] = electricity.footprint()/10
		context['strategy_table'] = strategy_table
	#	desired_model = pull_user_info('natural gas')
	#	desired_model.attribute
	#	desired.model.method(desired_model.attr)
		return render(request, "interview/strategies.html", context)