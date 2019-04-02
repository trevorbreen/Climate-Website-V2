from .parameters import carbon_footprint
#New Survey Questions

#How many holidays do you take per year?
#How mnay shifts per week do you work? 
#How many hours spent on an intercity bus per month?

#New Parameters
# cal/kg for foods
# fuel types/effiencies for public transit,
# airfreight kg/km


#Transportation
def increase_fuel_efficiency(yearly_distance_driven, fuel_type):
	increase_in_efficiency_per_km = (old_litres_per_hundred_km - new_litres_per_hundred_km) * 100
	return increase_in_efficiency_per_km * carbon_footprint[fuel_type] *  yearly_distance_driven  

def reduce_commute(old_distance_to_work_city, new_distance_to_work_city, new_distance_to_work_freeway, old_distance_to_work_freeway shifts_per_week, city_litres_per_hundred_km, freeway_litres_per_hundred_km, fuel_type):
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
:
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


def yearly_km_travelled(bus_journeys_per_week, average_bus_journey_time, avg_bus_speed, avg_train_speed, distance_by_car):
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



def website(request, attribute):
	#could pass a dictionary of kwargs 
	print(request.attribute)
	#might also work for class (not instance)