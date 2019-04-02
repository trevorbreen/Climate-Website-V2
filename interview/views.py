#Each view lives at a URL, thus, if you want to access a vew, you have to say where it lives in the urls.py directory of the app
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import all_forms_get, all_forms_post 
from django.forms import modelformset_factory
from .models import  Profile, Food, Vehicle 
from .models import Rideshare, Flight, Transit, Bicycle
from .models import  Residence, Appliances, Trash, NaturalGas, Electricity


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'interview/signup.html'

def home(request):
	return render(request, 'interview/home.html')

def results(request):
	return render(request, 'interview/results.html')


class Survey(generic.TemplateView):

	def post(self, request, subject):
		"""Adds current user and saves information from form to database"""
		form = all_forms_post(subject, request.POST)
		if form.is_valid():
			modified_form = form.save(commit=False)
			modified_form.user = request.user
			modified_form.save()
			return HttpResponseRedirect(request.META['HTTP_REFERER'])
		else:
			print('form is not valid')
			return HttpResponseRedirect(request.META['HTTP_REFERER'])		

	def get(self, request, subject):
		"""Sends all forms to the template as variables, 
		as well as additional information from their profile (unless they're creating one) """
		if subject != 'profile':
			context = {
				'number_of_vehicles': range(request.user.profile.number_of_vehicles),
				'number_of_flights' : range(request.user.profile.number_of_flights),
				'number_of_residences': range(request.user.profile.number_of_residences),
				'user_bikes': request.user.profile.rides_bike,
				'user_rideshares': request.user.profile.uses_rideshare,
				'user_takes_public_transit': request.user.profile.takes_public_transit,
			}
			all_forms_get.update(context)
			print(all_forms_get['bicycle'])
		return render(request, f"interview/{subject}.html", all_forms_get)

def formset_test(request):
	TestFormSet = modelformset_factory(Flight, exclude=('user',), extra=1, max_num = 5)
	if request.method == 'POST':
		form = TestFormSet(request.POST)
		print("Post requst")
		if form.is_valid():
			print('form is valid')
			modified_forms = form.save(commit=False)
			for instance in modified_forms:
				instance.user = request.user
				instance.save()
				print('form is saved')
			return HttpResponseRedirect(request.META['HTTP_REFERER'])
		else:
			print('form is not valid')
			return HttpResponseRedirect(request.META['HTTP_REFERER'])	
	else:
		test_formset = TestFormSet(queryset=Flight.objects.filter(user=request.user))
		return render(request, "interview/test.html", {'test_formset': test_formset})


all_models = {
	"profile": Profile,
	"vehicle": Vehicle,
	"rideshare": Rideshare,
	"flight": Flight,
	"transit": Transit,
	"bicycle": Bicycle,
	"residence": Residence,
	"appliances": Appliances,
	"trash": Trash,
	"natural_gas": NaturalGas,
	"electricity": Electricity,
	"food": Food,
	}
all_formsets = {
	"profile": modelformset_factory(Profile, exclude=('user',), extra=1, max_num = 1),
	"vehicle": modelformset_factory(Vehicle, exclude=('user',)),
	"rideshare": modelformset_factory(Rideshare, exclude=('user',), max_num = 1),
	"flight": modelformset_factory(Flight, exclude=('user',)),
	"transit": modelformset_factory(Transit, exclude=('user',), max_num = 1),
	"bicycle": modelformset_factory(Bicycle, exclude=('user',), max_num = 1),
	"residence": modelformset_factory(Residence, exclude=('user',), max_num = 1),
	"appliances": modelformset_factory(Appliances, exclude=('user',), max_num = 1),
	"trash": modelformset_factory(Trash, exclude=('user',), max_num = 1),
	"natural_gas": modelformset_factory(NaturalGas, exclude=('user',), max_num = 1),
	"electricity": modelformset_factory(Electricity, exclude=('user',), max_num = 1),
	"food": modelformset_factory(Food, exclude=('user',), max_num = 1),
	}

class GeneralCase(generic.TemplateView):

	def get(self, request, subject):
		form_set = all_formsets[subject]
		user_forms = form_set(queryset=all_models[subject].objects.filter(user=request.user))
		return render(request, "interview/generalcase.html", {'user_forms': user_forms, 'subject': subject})

	def post(self, request, subject):
		form_set = all_formsets[subject]
		form = form_set(request.POST)
		if form.is_valid():
			modified_forms = form.save(commit=False)
			for instance in modified_forms:
				instance.user = request.user
				instance.save()
				print('forms are saved')
			return HttpResponseRedirect(request.META['HTTP_REFERER'])
		else:
			print('form is not valid')
			return HttpResponseRedirect(request.META['HTTP_REFERER'])	

class Residence(generic.TemplateView):
#This approach works fine when a person has only one residence, however, issues will arise if they have two
#To account for this case, we will need to set max_num = request.user.number_of_residences
#However, when we do X.objects.filter(user=request.user) it won't return a unique value which could pose a problem
#One way to get around that would be to order by primary key, but how would we do that?
#Also, maybe Django will figure it out if there are multiple ones (we can try it right now)
	def get(self, request, *subject):
		residence = modelformset_factory(Residence, exclude=('user',), extra=1, max_num = 1)
		appliances = modelformset_factory(Appliances, exclude=('user',), extra=1, max_num = 1)
		electricity = modelformset_factory(Electricity, exclude=('user',), extra=1, max_num = 1)
		natural_gas = modelformset_factory(NaturalGas, exclude=('user',), extra=1, max_num = 1)
		trash = modelformset_factory(Trash, exclude=('user',), extra=1, max_num = 1)
		form_set = {
		'residence': residence(queryset=Residence.objects.filter(user=request.user)),
		'appliances': appliances(queryset=Appliances.objects.filter(user=request.user)),
		'electricity': electricity(queryset=Electricity.objects.filter(user=request.user)),
		'natural_gas': natural_gas(queryset=NaturalGas.objects.filter(user=request.user)),
		'trash': trash(queryset=Trash.objects.filter(user=request.user)),
		}
		return render(request, "interview/residence.html", form_set)

	def post(self, request, subject):
		Subject = all_models[subject]
		print(Subject)
		form_set = modelformset_factory(Subject, exclude=('user',), extra=1, max_num = 1)
		form = form_set(request.POST)
		if form.is_valid():
			modified_forms = form.save(commit=False)
			for instance in modified_forms:
				instance.user = request.user
				instance.save()
				print('form is saved')
			return HttpResponseRedirect(request.META['HTTP_REFERER'])
		else:
			print('form is not valid')
			return HttpResponseRedirect(request.META['HTTP_REFERER'])	


# class Residence(generic.TemplateView):
# 	def get(self, request, Subject):
# 		form_set = modelformset_factory(Subject, exclude=('user',), extra=1, max_num = 1)
# 		user_forms = form_set(queryset=Subject.objects.filter(user=request.user))
# 		return render(request, f"interview/{Subject.lower()}.html", {'user_forms': user_forms, 'Subject': Subject,})
# 	def post(self, request, Subject):
# 		form_set = modelformset_factory(Subject, exclude=('user',), extra=1, max_num = 1)
# 		form = form_set(request.POST)
# 		if form.is_valid():
# 			modified_form = form.save(commit=False)
# 			modified_form.user = request.user
# 			modified_form.save()
# 			return HttpResponseRedirect(request.META['HTTP_REFERER'])
# 		else:
# 			print('form is not valid')
# 			return HttpResponseRedirect(request.META['HTTP_REFERER'])	
# #POST
# # FormSet = all_forms(Subject)
# # form = TestFormSet(request.POST)
# # #GET
# TestFormSet(queryset=Subject.objects.filter(user=request.user))
# #Needs to be imported from Forms, also, there is a problem with the residence ones - subject.objects.filter is going to give you an extra natgas form for your residence 
# #Could split up the forms into 4 different views - profile, transportation, residence and food - would make templates simpler and get allow us to identify request.user.residence or something
# def all_forms(subject, number_of_vehicles, number_of_flights, number_of_residences):
# 	all_forms = {
# 	"Vehicle": modelformset_factory(Vehicle, exclude=('user',), extra=1, max_num = number_of_vehicles),
# 	"Rideshare": modelformset_factory(Rideshare, exclude=('user',), extra=1, max_num = 1),
# 	"Flight": modelformset_factory(Flight, exclude=('user',), extra=1, max_num = number_of_flights),
# 	"Transit": modelformset_factory(Transit, exclude=('user',), extra=1, max_num = 1),
# 	"Bicycle": modelformset_factory(Bicycle, exclude=('user',), extra=1, max_num = 1),
# 	"Residence": modelformset_factory(Residence, exclude=('user',), extra=1, max_num = number_of_residences),
# 	"Appliances": modelformset_factory(Appliances, exclude=('user',), extra=1, max_num = number_of_residences),
# 	"Trash": modelformset_factory(Trash, exclude=('user',), extra=1, max_num = number_of_residences),
# 	"NaturalGas": modelformset_factory(NaturalGas, exclude=('user',), extra=1, max_num = number_of_residences),
# 	"Electricity": modelformset_factory(Electricity, exclude=('user',), extra=1, max_num = number_of_residences),
# 	"Food": modelformset_factory(Food, exclude=('user',), extra=1, max_num = 1),
# 	}
# 	return all_forms[subject]
