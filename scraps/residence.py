from django.db import models
from .profile import Questions
from .parameters import carbon_footprint
from decimal import Decimal
from .profile import Strategy

class Residence(models.Model):
	utilities_included = models.BooleanField("Are utilities included in your rent?", default = False)
	electricity_bills = models.BooleanField("Can you get access to your electricity bill?", default = False)
	renewable_energy_share = models.IntegerField("What percentage of your energy comes from renewables?", default=12)
	biogas_share = models.IntegerField("What percentage of your natural gas comes from biogas?", default=0)
	gas_bills = models.BooleanField("Can you get access to your gas bill?", default = False)
	residents = models.IntegerField("How many people live in this residence?", default=1)
	size = models.IntegerField("How many square feet is this residence?", default=1000)
	housing_cost = models.IntegerField("What is your monthly rent or mortgage on this property?", default=1000)
	able_to_move = models.BooleanField("Is it feasible for you to change residences in the next year or so?", default = False)
	#Building Type 
	DETACHEDHOUSE, HIGHRISE, MULTIUNIT, WALKUP = 'detached',  'highrise apartment', 'multi-unit', 'walkup apartment'
	building_type_choices = ((DETACHEDHOUSE, 'detached house'),
	 										(HIGHRISE, 'apartment or condo'),
	 										(MULTIUNIT, 'multi-unit'),
	 										(WALKUP, 'walk-up apartment'))
	building_type = models.CharField(max_length  = 50, choices = building_type_choices, default = DETACHEDHOUSE)
	#Ownership
	OWNED, RENTINGLANDLORD, RENTINGCORPORATION, LIVINGWITHFAMILY = 'owned', 'landlord', 'corporation', 'family'
	ownership_type_choices = ((OWNED, 'homeowner'),
												(RENTINGLANDLORD, 'renting from a private landlord or owner'),
												(RENTINGCORPORATION, 'renting from a corporation or other organization'),
												(LIVINGWITHFAMILY, 'living with family'))
	owernship_type = models.CharField(max_length  = 50, choices = ownership_type_choices, default=RENTINGCORPORATION)

	def footprint(self, total_lifetime_footprint = 80_000, years_per_lifetime = 50):
		return total_lifetime_footprint / years_per_lifetime

class Utility(Questions):
	class Meta:
		abstract = True
	units = 'units'
	utility = 'utility'
	months = [january, february, march, april,
					 may, june, july, august, september,
					 october, november, december]
	#how do I write this for real?
	for month in months:
		month = models.IntegerField(f"How many {self.units} of {self.utility} did your residence use in January?")
	month_costs = [january_cost, february_cost, march_cost, april_cost,
							 may_cost, june_cost, july_cost, august_cost,
							 september_cost, october_cost, november_cost, december_cost]
	for month in month_costs:
		month_cost = models.DecimalField(f"How much was your {self.__str__()} bill in January?", max_digits=10, decimal_places=2)

	def average_monthy_cost(self):
		total_cost = 0
		attributes = vars(self)
		for monthly_cost in attributes:
			if isinstance(monthly_cost, Decimal):
				print(monthly_cost)
				total_cost += attributes[monthly_cost]
		return total_cost/12

class NaturalGas(Utility):
	units = 'gigajoules (GJ)'
	utility = 'natural gas'

	def footprint(self):
		"""In this model, costs are coded as decimals and gigajoules are coded as decimals, so we go through all attributes and add the integers (i.e kwh) up to get total consumption. Note that id and user_id are stored as integers so we ignore them with the if statement. Pretty hacky. """
		total_consumption = 0
		attributes = vars(self)
		for monthly_consumption in attributes:
			if monthly_consumption not in {'id', 'user_id'} and isinstance(attributes[monthly_consumption], int):
				total_consumption += attributes[monthly_consumption]
		return total_consumption * carbon_footprint['GJ natural gas']

class Electricity(Utility):
	units = 'kilowatt hours (kwh)'
	utility = 'electricity'

	def footprint(self):
		"""In this model, costs are coded as decimals and kwh are coded as integers, s0we go through all attributes and add the integers (i.e kwh) up to get total consumption. Note that id and user_id are stored as integers so we ignore them with the if statement. Pretty hacky. """
		total_consumption = 0
		attributes = vars(self)
		for monthly_consumption in attributes:
			if monthly_consumption not in {'id', 'user_id'} and isinstance(attributes[monthly_consumption], int):
				total_consumption += attributes[monthly_consumption]
		return total_consumption * carbon_footprint['kwh of electricity']

#class Water(Utility):
#	units = 'cubic metres (m^3)'
 #	utility = 'water'
# 		def footprint(self):
# 		"""In this model, costs are coded as decimals and kwh are coded as integers, s0we go through all attributes and add the integers (i.e kwh) up to get total consumption. Note that id and user_id are stored as integers so we ignore them with the if statement. Pretty hacky. """
# 		total_consumption = 0
# 		attributes = vars(self)
# 		for monthly_consumption in attributes:
# 			if monthly_consumption not in {'id', 'user_id'} and isinstance(attributes[monthly_consumption], int):
# 				total_consumption += attributes[monthly_consumption]
# 		return total_consumption * carbon_footprint['m3 water']

class Trash(models.Model):
	garbage_bin_volume = models.IntegerField("How many litres does your trash bin hold?")
	garbage_bin_fill_time = models.IntegerField("How many days does it usually take before you need to take out the trash?")

	def footprint(self, carbon_per_kg=0.5, pounds_per_cubic_yard=764.5):
		litres_per_cubic_yard = 764.5
		kilograms_per_pound = 1/2.2
		carbon_per_litre = carbon_per_kg * (pounds_per_cubic_yard *kilograms_per_pound)/ litres_per_cubic_yard
		garbage_fills_per_year = 365/self.garbage_bin_fill_time
		return carbon_per_litre * self.garbage_bin_volume * garbage_fills_per_year


	
class TrashStrategy(Strategy):
	def reduce_food_waste(percentage, weekly_food_consumption):
		pass
	
class ElectricityStrategy(Strategy):
	def increase_renewable_energy_share(increase_in_renewable_share, monthly_electricity_consumption):
		return monthly_electricity_consumption * carbon_footprint['electricity'] * increase_in_renewable_share

	def replace_lights_with_led():
		pass

	def hang_clothes_to_dry():
		electricity_averted = electricity_per_load
		money = electricity_per_load * electricity_price
		
		return (carbon, money, time)

	def wash_in_cold_water():
		pass

	def energy_efficient_refridgerator():
		pass

	def insulate_attic():
		pass

	def reseal_doors_and_windows():
		pass

	def shorten_showers():
		pass

	def fewer_baths():
		pass

	def solar_panels():
		pass


class NaturalGasStrategy(Strategy):
	def turn_down_thermostat(temperature_reduction, hours_per_day):
		pass
	def lower_boiler_temperature():
		pass

	def increase_biogas_share(increase_in_biogas_share, monthly_gas_consumption):
		return monthly_gas_consumption * carbon_footprint['natural gas'] * increase_in_biogas_share

	def increase_boiler_efficiency():
		pass