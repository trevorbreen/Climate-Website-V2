from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.conf import settings
from .parameters import carbon_footprints

# Create your models here.
class CustomUser(AbstractUser):
	user_type = 'basic'
	def __str__(self):
		return self.username

class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
	MALE = 'm'
	FEMALE = 'f'
	PREFERNOTTOSAY = 'n'
	sex_choices = ((MALE, 'male'), (FEMALE, 'female'), (PREFERNOTTOSAY, 'I prefer not to say'))
	age = models.IntegerField("What is your age?", blank = True, null=True)
	sex = models.CharField("What is your biological sex (used for food intake estimation)?", max_length = 50, choices = sex_choices, blank = True, null=True)
	annual_income = models.IntegerField("What is your annual income before taxes?", blank = True, null=True)
	savings = models.IntegerField("How much money do you save on a yearly basis? Use negative numbers to represent net borrowing.", blank = True, null=True)
	hours_worked = models.IntegerField("How many hours do you spend working in a typical week?", blank = True, null=True)
	#methodsOneToOneField
	def __str__(self):
		return self.user

class Survey(models.Model):
	electricity = models.DecimalField('how many kwh of electricity do you use per month?', max_digits=10, decimal_places=2)
	natgas = models.DecimalField('how many GJ of natural gas do you use per month?', max_digits=10, decimal_places=2)
	gasoline = models.DecimalField('how many litres of gasoline do you use per month?',max_digits=10,	decimal_places=2)
	user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
	
	def __str__(self):
		return str(self.user)
		
#Transportation Databases
class Transportation(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
	vehicles_owned = models.IntegerField("How many vehicles do you own?")
	flights_taken = models.IntegerField("How many flights did you take last year?")
	use_rideshare = models.BooleanField("Do you carpool, use taxis, or use ridesharing services?")
	ride_public_transit = models.BooleanField("Do you use public transit?")
	own_summer_bike = models.BooleanField("Do you own a bike that can be used when there is no snow on the ground?")
	own_winter_bike = models.BooleanField("Do you own a bike that can be used when there is snow on the ground?")
	distance_to_work = models.IntegerField("How many kilometers from your house to your workplace?")
	#methods
	def __str__(self):
		return self.user + 'transportation info'

class Vehicle(models.Model):
	transportation = models.ForeignKey(Transportation, on_delete=models.CASCADE, null=True)
	DIESEL = 'diesel'
	GASOLINE = 'gasoline'
	fuel_type_choices = ((DIESEL, 'diesel'),(GASOLINE, 'gasoline'))
	fuel_type =models.CharField(max_length  = 50, choices = fuel_type_choices, default = 'gasoline')
	fuel_economy_city = models.DecimalField("How many L/100 km does your vehicle get in the city?", max_digits=10, decimal_places=2) 
	fuel_economy_highway = models.DecimalField("How many L/100 km does your vehicle get on the highway?", max_digits=10, decimal_places=2)
	km_driven_city = models.IntegerField("How many kilometers do you drive in the city with this vehicle during a typical month?")
	km_driven_highway = models.IntegerField("How many kilometers do you drive on the freeway with this vehicle during a typical month?")
	fuel_ups = models.DecimalField("How many full tanks of gas do you put in your vehicle during a typical month? Decimals are allowed.", max_digits = 10, decimal_places = 2)
	tank_size = models.IntegerField("How many litres of gasoline does your tank hold?")
	vehicle_cost = models.IntegerField("How much do you spend on auto payments, insurance, registration and repairs for this vehicle in a typical year?")
	fuel_cost = models.IntegerField("How much do you spend on fuel in a typical month?")
	#methods
	def __str__(self):
		return self.transportation.user + 'vehicle info'
	def footprint(self):
		if self.fuel_type == 'diesel':
			return self.fuel_ups*self.tank_size*carbon_footprints['litre of diesel']
		else:
			return self.fuel_ups*self.tank_size*carbon_footprints['litre of gasoline']

class Rideshare(models.Model):
	transportation = models.ForeignKey(Transportation, on_delete=models.CASCADE, null=True)
	journeys = models.IntegerField("How often do you use cabs or ridesharing services in a typical month?")
	journey_time = models.IntegerField("When you use cabs or ridesharing services, how many minutes is a typical journey?")
	cost = models.IntegerField("How much do you spend on cab fare and ride sharing services in a typical month?")
	#methods
	def __str__(self):
		return self.transportation.user + 'Rideshare info'
	def footprint(self, avg_vehicle_speed, avg_fuel_economy):
		distance_travelled = self.journeys*self.journey_time*avg_vehicle_speed
		fuel_used = distance_travelled * avg_fuel_economy
		return fuel_used *carbon_footprints['litre of gasoline']

class Flight(models.Model):
	transportation = models.ForeignKey(Transportation, on_delete=models.CASCADE, null=True)
	length = models.DecimalField("How many hours was this flight?", max_digits=10, decimal_places=2)
	round_trip = models.BooleanField("was this flight round trip?", null=True)
	cost = models.IntegerField("How much did this flight cost?")
	#methods
	def __str__(self):
		return self.transportation.user + 'flight info'
	def footprint(self):
		if self.round_trip:
			return self.length * carbon_footprints['hour of flight']

class Transit(models.Model):
	transportation = models.ForeignKey(Transportation, on_delete=models.CASCADE, null=True)
	train_journeys = models.IntegerField("How many times do you ride the train on a typical week?")
	train_journey_time = models.IntegerField("When you ride the train, how many minutes is a typical journey?")
	bus_journeys = models.IntegerField("How many times do you ride the bus on a typical week?")
	bus_journey_time = models.IntegerField("When you ride the bus, how many minutes is a typical journey?")
	cost = models.IntegerField("How much do you spend on transit costs in a typical month?")
	#methods
	def __str__(self):
		return self.transportation.user + 'public transit info'
	def footprint(self):
		pass

class Bicycle(models.Model):
	transportation = models.ForeignKey(Transportation, on_delete=models.CASCADE, null=True)
	journey_time = models.IntegerField("When you ride the bike, how many minutes is a typical journey?")
	spring_journeys = models.IntegerField("How many journeys do you take on your bike in a typical week from April to May?")
	summer_journeys = models.IntegerField("How many journeys do you take on your bike in a typical week from June to August?")
	autumn_journeys = models.IntegerField("How many journeys do you take on your bike in a typical week from September to October?")
	winter_journeys = models.IntegerField("How many journeys do you take on your bike in a typical week from November to March?")
	#methods
	def __str__(self):
		return self.transportation.user + 'bicycle info'
	def footprint(self, calories_per_km, carbon_per_calorie, avg_bike_speed):
		distance = avg_bike_speed * self.journey_time *(self.spring_journeys/6 + self.summer_journeys/4 + self.autumn_journeys /6 +self.winter_journeys*(5/12))
		calories = distance * calories_per_km
		return carbon_per_calorie * calories


#Household Databases
class Household(models.Model):
	user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
	utilities_included = models.BooleanField("Are utilities included in your rent?")
	electricity_bills = models.BooleanField("Can you get access to your electricity bill?", null=False)
	renewable_energy_share = models.IntegerField("What percentage of your energy comes from renewables?", default=12.3)
	biogas_share = models.IntegerField("What percentage of your natural gas comes from biogas?", default=0)
	gas_bills = models.BooleanField("Can you get access to your electricity bill?" ,null=False)
	residents = models.IntegerField("How many people share this residence?")
	size = models.IntegerField("How many square feet is this residence?")
	housing_cost = models.IntegerField("What is your monthly rent or mortgage on this property?")
	able_to_move = models.BooleanField("Is it feasible for you to change residences in the next year or so?")
	#Building Type 
	DETACHEDHOUSE= 'detached'
	HIGHRISE = 'apartment'
	MULTIUNIT = 'multi'
	WALKUP = 'walkup'
	building_type_choices = ((DETACHEDHOUSE, 'detached house'), (HIGHRISE, 'apartmnet or condo'), (DETACHEDHOUSE, 'detached house'), (WALKUP, 'walk up apartment'))
	building_type = models.CharField(max_length  = 50, choices = building_type_choices)
	#Ownership
	OWNED = 'owned'
	RENTINGLANDLORD = 'landlord'
	RENTINGCORPORATION = 'corporation'
	LIVINGWITHFAMILY = 'family'
	ownership_type_choices = ((OWNED, 'homeowner'),(RENTINGLANDLORD, 'renting from a private landlord or owner'),(RENTINGCORPORATION, 'renting from a corporation or other organization'),(LIVINGWITHFAMILY, 'living with family'))
	owernship_type = models.CharField(max_length  = 50, choices = ownership_type_choices)
	#methods
	def __str__(self):
		return self.user + 'housing info'
	def footprint(self):
		pass

class Appliances(models.Model):
	household = models.ForeignKey(Household, on_delete=models.CASCADE, null=True)
	FRIDGE = 'fridge'
	DEEPFREEZE = 'freezer'
	WASHER = 'washer'
	DRYER = 'dryer'
	STOVE = 'stove'
	OVEN = 'oven'
	MICROWAVE = 'microwave'
	COMPUTER = 'computer'
	TELEVISION = 'television'
	FURNACE = 'furnace'
	BOILER = 'boiler'
	AIRCONDITIONING = 'ac'
	LIGHTS = 'lights'
	SHOWER = 'shower'
	appliances_choices = ((FRIDGE, 'fridge'),(DEEPFREEZE, 'seperate freezer'), (WASHER, 'washing machine'), (DRYER, 'drying machine'), (STOVE, 'stovetop'), (OVEN, 'oven'), (MICROWAVE, 'microwave'), (COMPUTER, 'computer'), (TELEVISION, 'television'), (FURNACE, 'furnace'), (BOILER, 'boiler'), (AIRCONDITIONING, 'air conditioning'), (LIGHTS, 'lights'), (SHOWER, 'shower'))
	appliances_in_residence = models.CharField(max_length  = 50, choices = appliances_choices)
	high_efficiency_appliances =  models.CharField(max_length  = 50, choices = appliances_choices)
	#methods
	def __str__(self):
		return self.user + 'appliance info'

class Trash(models.Model):
	household = models.ForeignKey(Household, on_delete=models.CASCADE, null=True)
	garbage_bin_volume = models.IntegerField("How many litres does your trash bin hold?")
	garbage_bin_fill_time = models.IntegerField("How many days does it usually take before you need to take out the trash?")
	#methods
	def __str__(self):
		return self.household.user + 'trash info'
	def footprint(self):
		pass

class NaturalGas(models.Model):
	household = models.ForeignKey(Household, on_delete=models.CASCADE, null=True)
	#consumption
	january_natural_gas = models.IntegerField("How many GJ of natural gas did your household use in January?")
	february_natural_gas = models.IntegerField("How many GJ of natural gas did your household use in February?")
	march_natural_gas = models.IntegerField("How many GJ of natural gas did your household use in March?")
	april_natural_gas = models.IntegerField("How many GJ of natural gas did your household use in April?")
	may_natural_gas = models.IntegerField("How many GJ of natural gas did your household use in May?")
	june_natural_gas = models.IntegerField("How many GJ of natural gas did your household use in June?")
	july_natural_gas = models.IntegerField("How many GJ of natural gas did your household use in July?")
	august_natural_gas = models.IntegerField("How many GJ of natural gas did your household use in August?")
	september_natural_gas = models.IntegerField("How many GJ of natural gas did your household use in September?")
	october_natural_gas = models.IntegerField("How many GJ of natural gas did your household use in October?")
	november_natural_gas = models.IntegerField("How many GJ of natural gas did your household use in November?")
	december_natural_gas = models.IntegerField("How many GJ of natural gas did your household use in December?")
	#costs
	january_cost = models.DecimalField("How much was your natural gas bill in January?", max_digits=10, decimal_places=2)
	february_cost = models.DecimalField("How much was your natural gas bill in February?", max_digits=10, decimal_places=2)
	march_cost = models.DecimalField("How much was your natural gas bill in March?", max_digits=10, decimal_places=2)
	april_cost = models.DecimalField("How much was your natural gas bill in April?", max_digits=10, decimal_places=2)
	may_cost = models.DecimalField("How much was your natural gas bill in May?", max_digits=10, decimal_places=2)
	june_cost = models.DecimalField("How much was your natural gas bill in June?", max_digits=10, decimal_places=2)
	july_cost = models.DecimalField("How much was your natural gas bill in July?", max_digits=10, decimal_places=2)
	august_cost = models.DecimalField("How much was your natural gas bill in August?", max_digits=10, decimal_places=2)
	september_cost = models.DecimalField("How much was your natural gas bill in September?", max_digits=10, decimal_places=2)
	october_cost = models.DecimalField("How much was your natural gas bill in October?", max_digits=10, decimal_places=2)
	november_cost = models.DecimalField("How much was your natural gas bill in November?", max_digits=10, decimal_places=2)
	december_cost = models.DecimalField("How much was your natural gas bill in December?", max_digits=10, decimal_places=2)
	#methods
	def __str__(self):
		return self.user + 'natural gas info'
	def average_monthy_natural_gas_consumption(self):
		total_consumption = 0
		for monthly_consumption in vars(self):
			if isinstance(monthly_consumption, int):
				total_consumption += monthly_consumption
		return total_consumption/12
	def average_monthy_natural_gas_cost(self):
		total_cost = 0
		for monthly_cost in vars(self):
			if isinstance(monthly_cost, float):
				total_cost += monthly_cost
		return total_cost/12
	def footprint(self):
		return self.average_monthy_natural_gas_consumption() * 12 * carbon_footprints['GJ of natural gas']

class Electricity(models.Model):
	household = models.ForeignKey(Household, on_delete=models.CASCADE, null=True)
	#consumption
	january_electricity = models.IntegerField("How many kwh of electricity did your household use in January?")
	february_electricity = models.IntegerField("How many kwh of electricity did your household use in February?")
	march_electricity = models.IntegerField("How many kwh of electricity did your household use in March?")
	april_electricity = models.IntegerField("How many kwh of electricity did your household use in April?")
	may_electricity = models.IntegerField("How many kwh of electricity did your household use in May?")
	june_electricity = models.IntegerField("How many kwh of electricity did your household use in June?")
	july_electricity = models.IntegerField("How many kwh of electricity did your household use in July?")
	august_electricity = models.IntegerField("How many kwh of electricity did your household use in August?")
	september_electricity = models.IntegerField("How many kwh of electricity did your household use in September?")
	october_electricity = models.IntegerField("How many kwh of electricity did your household use in October?")
	november_electricity = models.IntegerField("How many kwh of electricity did your household use in November?")
	december_electricity = models.IntegerField("How many kwh of electricity did your household use in December?")
	#costs
	january_cost = models.DecimalField("How much was your electricity bill in January?", max_digits=10, decimal_places=2)
	february_cost = models.DecimalField("How much was your electricity bill in February?", max_digits=10, decimal_places=2)
	march_cost = models.DecimalField("How much was your electricity bill in March?", max_digits=10, decimal_places=2)
	april_cost = models.DecimalField("How much was your electricity bill in April?", max_digits=10, decimal_places=2)
	may_cost = models.DecimalField("How much was your electricity bill in May?", max_digits=10, decimal_places=2)
	june_cost = models.DecimalField("How much was your electricity bill in June?", max_digits=10, decimal_places=2)
	july_cost = models.DecimalField("How much was your electricity bill in July?", max_digits=10, decimal_places=2)
	august_cost = models.DecimalField("How much was your electricity bill in August?", max_digits=10, decimal_places=2)
	september_cost = models.DecimalField("How much was your electricity bill in September?", max_digits=10, decimal_places=2)
	october_cost = models.DecimalField("How much was your electricity bill in October?", max_digits=10, decimal_places=2)
	november_cost = models.DecimalField("How much was your electricity bill in November?", max_digits=10, decimal_places=2)
	december_cost = models.DecimalField("How much was your electricity bill in December?", max_digits=10, decimal_places=2)
	#methods
	def __str__(self):
		return self.household.user + 'electricity info'
	def average_monthy_electricity_consumption(self):
		total_consumption = 0
		for monthly_consumption in vars(self):
			if isinstance(monthly_consumption, int):
				total_consumption += monthly_consumption
		return total_consumption/12
	def average_monthy_electricity_cost(self):
		total_cost = 0
		for monthly_cost in vars(self):
			if isinstance(monthly_cost, float):
				total_cost += monthly_cost
		return total_cost/12
	def footprint(self):
		return self.average_monthy_electricity_consumption() * 12 * carbon_footprints['kwh of electricity']


#Food Databases
class Food(models.Model):
	user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
	OMNIVORE = 'omnivore'
	NOBEEF = 'beefless'
	VEGGIE = 'vegetarian'
	VEGAN = 'vegan'
	diet_choices = ((OMNIVORE, 'omnivore'), (NOBEEF, 'omnivore but no beef'), (VEGGIE, 'vegetarian (eggs and cheese but no meat)'), (VEGAN, 'vegan (no animal products'))
	diet =  models.CharField("What is the best way to describe your diet?", max_length  = 50, choices=diet_choices)
	ALOTMORE = 1.5
	SOMEWHATMORE = 1.25
	ABOUTTHESAME = 1
	SOMEWHATLESS = 0.75
	ALOTLESS = 0.5
	food_intake_choices = ((ALOTMORE, 'a lot more than other people my age'), (SOMEWHATMORE, 'somewhat more than other people my age'), (ABOUTTHESAME, 'about the same as other people my age'), (SOMEWHATLESS, 'somewhat less than other people my age'), (ALOTLESS, 'a lot less than other people my age'))
	food_intake =  models.CharField("What is the best way to describe the amount of food you eat?", max_length  = 50, choices=food_intake_choices)
	local_share = models.IntegerField("What percentage of your diet is composed of locally sourced food?")
	seasonal = models.BooleanField("Do you buy fruits and vegtables out of season?")
	grocery_cost = models.IntegerField("How much do you spend on groceries in a typical week?")
	restaurant_cost = models.IntegerField("How much do you spend on food from restaurants in a typical week?")
	#methods
	def __str__(self):
		return self.user + 'food info'
	def footprint(self):
		if self.diet == 'omnivore':
			return carbon_footprints['omnivore diet']
		if self.diet == 'no beef':
			return carbon_footprints['no beef diet']
		if self.diet == 'vegetarian':
			return carbon_footprints['vegetarian diet']
		if self.diet == 'vegan':
			return carbon_footprints['vegan diet']
