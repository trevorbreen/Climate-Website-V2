from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.conf import settings
from .parameters import carbon_footprint
from interview.forms import all_models

class CustomUser(AbstractUser):
	user_type = 'basic'
	def __str__(self):
		return self.username

class Questions(models.Model):
	class Meta:
		abstract = True
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null = True)
	def __str__(self):
		return str(self.__class__.__name__) + str(self.id)

class Strategy(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
	def footprint_model(self):
		return all_models[self.__str__().replace('Strategy')] #feels pretty janky
	def __str(self):
		return str(self.__class__.__name__)

class Profile(Questions):
	MALE = 'm'
	FEMALE = 'f'
	PREFERNOTTOSAY = 'n'
	sex_choices = ((MALE, 'male'), (FEMALE, 'female'), (PREFERNOTTOSAY, 'I prefer not to say'))
	age = models.IntegerField("What is your age?", blank = True, null=True)
	sex = models.CharField("What is your biological sex (used for food intake estimation)?", max_length = 50, choices = sex_choices, blank = True, null=True)
	annual_income = models.IntegerField("What is your annual income before taxes?", blank = True, null=True)
	savings = models.IntegerField("How much money do you save on a yearly basis? Use negative numbers to represent net borrowing.", blank = True, null=True)
	hours_worked = models.IntegerField("How many hours do you spend working in a typical week?", blank = True, null=True)
	shifts_per_week = models.IntegerField("How many shifts do you work per week?", blank= True, null = True)
	number_of_residences = models.IntegerField("How many residences do you have?", blank = True, null=True)
	number_of_vehicles = models.IntegerField("How many vehicles do you own?", blank= True, null = True)
	number_of_flights = models.IntegerField("How many flights did you take last year?", blank= True, null = True)
	uses_rideshare = models.BooleanField("Do you carpool, use taxis, or use ridesharing services?", blank= True, null = True)
	takes_public_transit = models.BooleanField("Do you use public transit?", blank= True, null = True)
	rides_bike = models.BooleanField("Do you get around on a bike?", blank= True, null = True)
	own_summer_bike = models.BooleanField("Do you own a bike that can be used when there is no snow on the ground?", blank= True, null = True)
	own_winter_bike = models.BooleanField("Do you own a bike that can be used when there is snow on the ground?", blank= True, null = True)
	distance_to_work = models.IntegerField("How many kilometers from your house to your workplace?", blank= True, null = True)
	#methodsOneToOneField
	def __str__(self):
		return str(self.user) # 'profile'
	def footprint(self):
		return self.annual_income * carbon_footprint['one dollar in alberta']
