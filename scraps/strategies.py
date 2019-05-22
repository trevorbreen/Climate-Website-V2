from django.db import models
from django.conf import settings
class Questions(models.Model):
	#For reparenting in later version
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null = True)
	def __str__(self):
		return str(self.__class__.__name__) + str(self.id)

class Commute(Questions):
#	automobiles = [(vehicles, vehicles.__str__()) for vehicles in all_models['vehicles'].objects.filter(user=request.user)]
#	vehicle_used = models.CharField("Which automobile do you use to commute?", choices=automobiles, blank=True, null=True)
	minutes_on_freeway = models.IntegerField("On average, how many minutes do you spend driving at freeway speeds (>80 km/h) during a one-way commute?")
	minutes_in_city = models.IntegerField("On average, how many minutes do you spend driving at city speeds (<80 km/h) during a one-way commute?")
	minutes_on_train =models.IntegerField("On average, how many minutes do you spend on the train during a one-way commute?")
	minutes_on_bus = models.IntegerField("On average, how many minutes do you spend bussing during a one-way commute?")
	minutes_on_bike = models.IntegerField("On average, how many minutes do you spend biking during a one-way commute?")
	commute_days_per_week = models.IntegerField("On average, how many days do you commute per week?")
	carpooling_passengers = models. IntegerField("On average, how many carpool passengers are there in a one-way commute?", helptext="enter 0 if you don't drive")
	# percentage_of_year = IntegerField("What percentage of your total commutes does this profile characterize?")

	def carbon_per_commute(self, Bike, Transit, Vehicle, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city, vehicle_used):
		bike_carbon = Bike.carbon_per_minute() * minutes_of_biking
		transit_carbon = Transit.average_carbon_per_minute(minutes_on_bus, minutes_on_train, minutes_of_waiting) * (minutes_on_bus + minutes_on_train + minutes_of_waiting)
		if vehicle_used == None:
			vehicle_carbon = 0 
		else:
			vehicle_carbon = Vehicle.average_carbon_per_minute(minutes_on_freeway, minutes_in_city)
		return sum(bike_carbon, transit_carbon, vehicle_carbon)

	def cost_per_commute(self, Bike, Transit, Vehicle, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city, transit_journeys_per_month, vehicle_used):
		bike_cost = Bike.cost_per_minute() * minutes_of_biking
		transit_cost = Transit.average_cost_per_minute(minutes_on_bus, minutes_on_train, minutes_of_waiting, transit_journeys_per_month) * (minutes_on_bus + minutes_on_train + minutes_of_waiting)
		if vehicle_used == None:
			vehicle_cost = 0 
		else:	
			vehicle_cost = Vehicle.average_cost_per_minute(minutes_on_freeway, minutes_in_city)
		return sum(bike_cost, transit_cost, vehicle_cost)
	def time_per_commute(self, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city):
		return sum(minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city)

	def carbon_per_month(self, Bike, Transit, Vehicle, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city, commutes_per_month, transit_journeys_per_month):
		return  commutes_per_month * self.cost_per_commute(Bike, Transit, Vehicle, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city, transit_journeys_per_month)

	def cost_per_month(self, Bike, Transit, Vehicle, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city, commutes_per_month, transit_journeys_per_month):
		return commutes_per_month *self.cost_per_commute(Bike, Transit, Vehicle, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city, transit_journeys_per_month)

	def minutes_per_commute(self, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city)	:
		return sum(minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city)

	def minutes_commuting_per_month(self, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city, commutes_per_week):
		return 4.35 * commutes_per_week * self.minutes_per_commute(minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city)


from .parameters import carbon_footprint
#New Survey Questions

#How many holidays do you take per year?
#How mnay shifts per week do you work? 
#How many hours spent on an intercity bus per month?

#New Parameters
# cal/kg for foods
# fuel types/effiencies for public transit,
# airfreight kg/km

def energy_consumed_by_boiler():
	pass
def replace_windows():
	pass
def insulate_attic():
	pass
def high_efficiency_furnace():
	pass
def air_sealing(age_of_house, upgrades=False, new_air_changes_per_hour=3):
	pass
def turn_down_thermostat(start_temp, end_temp, mean_average_ambient_temperature):
	pass


#Obvious Ones
def shorten_drive_commute_ten_minutes(minutes_in_city, minutes_on_freeway, commute_days_per_week, weeks_of_vacation=3, Vehicle=None):
	if Vehicle==None:
		return (0,0,0)
	carbon_per_old_commute = Vehicle.average_carbon_per_minute(minutes_in_city, minutes_on_freeway) * sum(minutes_in_city, minutes_on_freeway)
	if minutes_on_freeway>10:
		minutes_on_freeway -= 10
	elif minutes_in_city>10: 
		minutes_in_city -= (10 - minutes_on_freeway)
		minutes_on_freeway = 0
	else:
		minutes_on_freeway, minutes_in_city = 0,0
	carbon_per_new_commute = Vehicle.average_carbon_per_minute(minutes_in_city, minutes_on_freeway) * sum(minutes_in_city, minutes_on_freeway)
	commutes_per_year = commute_days_per_week * 2 * (52-weeks_of_vacation)

	carbon = commutes_per_year * (carbon_per_old_commute-carbon_per_new_commute)
	hours_saved = commutes_per_year * 10/60
	fuel_savings = commutes_per_year * Vehicle.average_dollars_per_minute(minutes_in_city, minutes_on_freeway) * sum(minutes_in_city, minutes_on_freeway)
	return (carbon, hours_saved, fuel_savings)
def transit_to_work():
	pass
# shorten commute by 10 minutes each way - fuel economy (highway, city) - 
# transit to work - time on bus + time on train
# bike to work - distance to work / 15.5
# increase fuel economy by 1 litre/100 km - driving distance last year

# No Beef - difference
# Go vegetarian - difference
# Go Vegan - difference
# buy veggies in season
# buy food locally

# increase household power efficiency by 10%
# reduce natural gas use
# increase share of renewable energy
# reduce household waste by 10 %

# one less round trip flight

#Transportation
def increase_fuel_efficiency(yearly_distance_driven, fuel_type, old_litres_per_hundred_km, new_litres_per_hundred_km):
	increase_in_efficiency_per_km = (old_litres_per_hundred_km - new_litres_per_hundred_km) * 100
	return increase_in_efficiency_per_km * carbon_footprint[fuel_type] *  yearly_distance_driven  

def reduce_commute(old_distance_to_work_city, new_distance_to_work_city, new_distance_to_work_freeway, old_distance_to_work_freeway, shifts_per_week, city_litres_per_hundred_km, freeway_litres_per_hundred_km, fuel_type):
	emissions_per_kilometre_city = carbon_footprint[fuel_type] * city_litres_per_hundred_km *100 #multiply by 100 to get litre per kilometre
	emissions_per_kilometre_freeway = carbon_footprint[fuel_type] * freeway_litres_per_hundred_km *100 #multiply by 100 to get litre per kilometre
	old_km_commuted_per_month_city = old_distance_to_work_city * shifts_per_week * 2 # multiply by 2 to get round trip
	new_km_commuted_per_month_city = new_distance_to_work_city * shifts_per_week *2
	old_km_commuted_per_month_freeway = old_distance_to_work_freeway * shifts_per_week * 2 
	new_km_commuted_per_month_freeway = new_distance_to_work_freeway * shifts_per_week *2
	old_emissions_per_month = emissions_per_kilometre_city * old_km_commuted_per_month_city + emissions_per_kilometre_freeway* old_km_commuted_per_month_freeway
	new_emissions_per_month = emissions_per_kilometre_city * new_km_commuted_per_month_city + emissions_per_kilometre_freeway* new_km_commuted_per_month_freeway
	return old_emissions_per_month - new_emissions_per_month

def transit_to_work(distance_to_work_driving, shifts_per_week, litres_per_hundred_km, fuel_type, distance_to_work_bussed, distance_to_work_trained):
	km_commuted_per_month = distance_to_work_driving * shifts_per_week * 2
	emissions_from_driving = km_commuted_per_month * litres_per_hundred_km *100 * carbon_footprint[fuel_type] 
	emissions_from_transit = distance_to_work_bussed * carbon_footprint['bus'] *2 + distance_to_work_trained * carbon_footprint['train'] *2
	return emissions_from_driving - emissions_from_transit

def bike_to_work(months_per_year, distance_to_work, shifts_per_week, fuel_type, gas_mileage, diet, calories_per_year):
	km_commuted_per_month = distance_to_work * shifts_per_week * 2
	emissions_from_driving = km_commuted_per_month * litres_per_hundred_km *100 * carbon_footprint[fuel_type] 
	carbon_per_calorie = carbon_footprint[diet]/calories_per_year
	emissions_from_biking = distance_to_work * calories_burned * carbon_per_calorie *2
	return emissions_from_driving - emissions_from_biking

def emissions_per_km (units_of_fuel_per_km, fuel_type):
	#could be used within the adjust_share_of_transportation function 
	return units_of_fuel_per_km * carbon_footprint[fuel_type] #what about busses and trains? 

def weekly_km_travelled_bus(bus_journeys_per_week, average_bus_journey_time, avg_bus_speed):
	return bus_journeys_per_week * average_bus_journey_time * avg_bus_speed 
def weekly_km_travelled_train(train_journeys_per_week, average_train_journey_time, avg_train_speed):
	return train_journeys_per_week * average_train_journey_time * avg_train_speed

def weekly_km_travelled_car(method, **kwargs):
	#Needs some way to verify that the appropriate arguments are passed given the method
	if method == 'fuel_ups':
		return fuel_ups_per_month * litres_per_tank * avg_litres_per_hundred_kilometres
	elif method == 'last maintenance/purchase':
		return  (current_odometer - odometer_at_purchase_or_maintenance) / years_since_purchase_or_maintenance
	elif method == 'yearly distance known':
		return known_distance_by_car


def yearly_km_travelled(bus_journeys_per_week, average_bus_journey_time, avg_bus_speed, train_journeys_per_week, average_train_journey_time, avg_train_speed, distance_by_car):
	distance_by_bus = bus_journeys_per_week * average_bus_journey_time * avg_bus_speed * 52 #52 weeks in a year
	distance_by_train = train_journeys_per_week * average_train_journey_time * avg_train_speed * 52 
	return distance_by_car + distance_by_train + distance_by_bus


def adjust_share_of_transportation(litres_per_hundred_km, fuel_type, avg_non_household_passengers, transit_type, percent_shifted, yearly_km_travelled):
	change_in_emissions_per_km = litres_per_hundred_km * carbon_footprint[fuel_type]/avg_non_household_passengers *100 - carbon_footprint[transit_type]
	return change_in_emissions_per_km * percent_shifted * yearly_km_travelled
#divide according to work, vacations, and chores/leisure

def add_person_to_carpool(litres_per_hundred_km_passenger_vehicle, fuel_type, preexisting_passengers):
	km_commuted_per_month = (distance_to_work + distance_to_passenger) * shifts_per_week * 2
	passenger_emissions_from_driving_avoided = km_commuted_per_month * litres_per_hundred_km *100 * carbon_footprint[fuel_type] 
	return passenger_emissions_from_driving_avoided / 2 # divide by 2 splits emission reductions evenly between passenger and driver

def one_fewer_hour_driving_highway(avg_speed, fuel_type, litres_per_hundred_km_freeway):
	return avg_speed * litres_per_hundred_km_freeway * carbon_footprint[fuel_type] *100

def one_fewer_hour_driving_city(avg_speed, fuel_type, litres_per_hundred_km_city):
	return avg_speed * litres_per_hundred_km_city * carbon_footprint[fuel_type] *100

def one_fewer_flight(length_of_flight):
	return length_of_flight * carbon_footprint['flight']

def one_hour_less_flight():
	return carbon_footprint['flight']

def one_less_vacation(distance_to_destination, avg_light_passenger_vehicle_litres_per_hundred_km):
	#Rests on the assumptiont that emissions from flying are about as much as emissions from driving per kilometer 
	return distance_to_destination *carbon_footprint['gasoline'] * avg_light_passenger_vehicle_litres_per_hundred_km * 100 *  2
	
def reduce_distance_to_vacation(fuel_type, litres_per_hundred_km_freeway, change_in_distance):
	return carbon_footprint[fuel_type] * litres_per_hundred_km_freeway * change_in_distance

def litres_per_hundred_km_avg(distance_driven_city, distance_driven_freeway, litres_per_hundred_km_freeway, litres_per_hundred_km_city):
	return (distance_driven_city * litres_per_hundred_km_city + distance_driven_freeway * litres_per_hundred_km_freeway)/ (distance_driven_city + distance_driven_freeway)

def yearly_distance_driven(litres_per_tank, fuel_ups_per_month, litres_per_hundred_km_avg):
	return litres_per_tank * fuel_ups_per_month / litres_per_hundred_km_avg

def swap_to_electric_car(litres_per_hundred_km_avg, fuel_type, kwh_per_hundred_km_avg, yearly_distance_driven, percent_renewable_gen):
	emissions_per_km_vehicle_one = carbon_footprint['fuel_type'] * litres_per_hundred_km_avg * 100 
	emissions_per_km_vehicle_two = carbon_footprint['electricity'] *(1-percent_renewable_gen) * kwh_per_hundred_km_avg * 100
	return (emissions_per_km_vehicle_one - emissions_per_km_vehicle_two) * yearly_distance_driven   


#Household
def reduce_food_waste(percentage, weekly_food_consumption):
	pass
def increase_renewable_energy_share(increase_in_renewable_share, monthly_electricity_consumption):
	return monthly_electricity_consumption * carbon_footprint['electricity'] * increase_in_renewable_share
def increase_biogas_share(increase_in_biogas_share, monthly_gas_consumption):
	return monthly_gas_consumption * carbon_footprint['natural gas'] * increase_in_biogas_share
def increase_boiler_efficiency():
	pass
def lower_boiler_temperature():
	pass
def replace_lights_with_led():
	pass
def hang_clothes_to_dry():
	pass
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
def turn_down_thermostat(temperature_reduction, hours_per_day):
	pass
def solar_panels():
	pass



#Food
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
	
#Finances
def green_bond():
	pass

def carbon_offset_per_tonne(tonnes):
	return tonnes
def carbon_offset_per_dollar(dollars, one_tonne_offset_cost):
	return one_tonne_offset_cost/dollars
