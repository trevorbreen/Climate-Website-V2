from django.db import models
from .profile import Questions, Strategy
from .parameters import carbon_footprint

class Food(Questions):
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
	food_intake_choices = ((ALOTMORE, 'a lot more than other people my age'),
										(SOMEWHATMORE, 'somewhat more than other people my age'),
										(ABOUTTHESAME, 'about the same as other people my age'),
										(SOMEWHATLESS, 'somewhat less than other people my age'),
										(ALOTLESS, 'a lot less than other people my age'))
	food_intake =  models.DecimalField("What is the best way to describe the amount of food you eat?", choices=food_intake_choices, max_digits=3, decimal_places=2)
	local_share = models.IntegerField("What percentage of your diet is composed of locally sourced food?")
	seasonal = models.BooleanField("Do you buy fruits and vegtables out of season?")
	grocery_cost = models.IntegerField("How much do you spend on groceries in a typical week?")
	restaurant_cost = models.IntegerField("How much do you spend on food from restaurants in a typical week?")
	def footprint(self):
		if self.diet == 'omnivore':
			return carbon_footprint['omnivore diet']
		if self.diet == 'no beef':
			return carbon_footprint['no beef diet']
		if self.diet == 'vegetarian':
			return carbon_footprint['vegetarian diet']
		if self.diet == 'vegan':
			return carbon_footprint['vegan diet']


class FoodStrategy(Strategy):
	def replace_food_kilogram(kg, current_food, substitute_food):
		carbon_difference_per_kilo = carbon_footprint[current_food]-carbon_footprint[substitute_food]
		return kg *(carbon_difference_per_kilo)

	def replace_food_calorie(calories, current_food, substitute_food, current_calories_per_kilogram, substitute_calories_per_kilogram):
		current_carbon_per_calorie= carbon_footprints[current_food]*current_calories_per_kilogram
		substitute_carbon_per_calorie = carbon_footprints[substitute_food]*substitute_calories_per_kilogram
		return calories*(current_carbon_per_calorie-substitute_carbon_per_calorie)
	def reduce_consumption_one_day(per_day_calorie_reduction, reduction_food):
		#This feels like its crossing a line - suggesting people should eat less
		return carbon_footprint[reduction_food] * per_day_calorie_reduction

	def reduce_share_of_airfreight_produce(total_produce_consumed, share_reduction, avg_distance_flown):
		emissions_per_kg_airfreight = avg_distance_flown * carbon_footprint['airfreight']
		total_kg_shifted = total_produce_consumed * share_reduction
		return total_kg_shifted * emissions_per_kg_airfreight

	
class FinanceStrategy(Strategy):	
	def green_bond():
		pass

	def carbon_offset_per_tonne(tonnes):
		return tonnes

	def carbon_offset_per_dollar(dollars, one_tonne_offset_cost):
		return one_tonne_offset_cost/dollars

