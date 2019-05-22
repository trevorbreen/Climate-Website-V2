from .parameters import carbon_footprint
from .profile import Questions

class Vehicles(Questions):
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
	def carbon_per_km(self, fuel_economy_city=None, fuel_economy_highway=None, city=True):
		if fuel_economy_city == None:
			fuel_economy_city = self.fuel_economy_city
		if fuel_economy_highway== None:
			fuel_economy_highway = self.fuel_economy_highway
		if city:
			litres_per_hunded_km = fuel_economy_city
		else:
			litres_per_hunded_km = fuel_economy_highway
		if self.fuel_type == 'diesel':
			carbon_per_litre = carbon_footprint['litre of diesel']
		if self.fuel_type == 'electicity':
			carbon_per_litre = carbon_footprint['kwh of electricity']
		else:
			carbon_per_litre = carbon_footprint['litre of gasoline']
		return litres_per_hunded_km * carbon_per_litre / 100
	def dollars_per_km(self, price_of_fuel= 1.20, city=True):
		if city:
			litres_per_hunded_km = self.fuel_economy_city
		else:
			litres_per_hunded_km = self.fuel_economy_highway
		return litres_per_hunded_km * price_of_fuel / 100
	def average_carbon_per_minute(self, average_city_km_per_h=38, average_freeway_km_per_h=100, minutes_in_city, minutes_on_freeway):
		minutes_per_hour = 60
		city_carbon = self.carbon_per_km(city=True) * (average_city_km_per_h/minutes_per_hour) * minutes_in_city
		freeway_carbon = self.carbon_per_km(city=False) * (average_freeway_km_per_h/minutes_per_hour) * minutes_on_freeway
		return (city_carbon + freeway_carbon)/(minutes_in_city + minutes_on_freeway)
	def average_dollars_per_minute(self, price_of_fuel=1.2, minutes_in_city, minutes_on_freeway): # does not include insurance, repair costs,
		minutes_per_hour = 60
		city_cost = self.dollars_per_km(price_of_fuel=price_of_fuel, city=True) * (average_city_km_per_h/minutes_per_hour) * minutes_in_city
		freeway_cost = self.dollars_per_km(price_of_fuel=price_of_fuel, city=False) * (average_freeway_km_per_h/minutes_per_hour) * minutes_on_freeway
		return (city_cost + freeway_cost)/(minutes_in_city + minutes_on_freeway)

	def total_impact(self, minutes_in_city, minutes_on_freeway, price_of_fuel=1.2):
		time_spent_driving = minutes_in_city + minutes_on_freeway
		average_carbon_per_minute = self.average_carbon_per_minute(minutes_in_city, minutes_on_freeway)
		average_dollars_per_minute = self.average_dollars_per_minute(price_of_fuel=price_of_fuel, minutes_in_city, minutes_on_freeway)
		carbon = average_carbon_per_minute * time_spent_driving
		cost = average_dollars_per_minute * time_spent_driving
		return (carbon, cost, time_spent_driving, average_carbon_per_minute, average_dollars_per_minute)


#the plan: create classes with methods to do footprint calculations, accept some time inputs for the commutes but give them methods for total footprints 
class Transit(Questions):
	bus_carbon_per_km = 0.15 * 0.6213
	bus_km_per_hour = 12.1 /  0.6213
	train_km_per_hour=30
	train_carbon_per_mile_uk = 0.19
	uk_carbon_per_kwh=0.49
	ab_carbon_per_kwh=carbon_footprint['kwh of electricity']
	fixed_cost = 0
	train_journeys = models.IntegerField("How many times do you ride the train on a typical week?")
	train_journey_time = models.IntegerField("When you ride the train, how many minutes is a typical journey?")
	bus_journeys = models.IntegerField("How many times do you ride the bus on a typical week?")
	bus_journey_time = models.IntegerField("When you ride the bus, how many minutes is a typical journey?")
	minutes_on_train = train_journey_time * train_journeys
	def carbon_per_km(self, bus):
		if bus== True:
			return self.bus_carbon_per_km
		else:
			carbon_from_electricity_conversion_factor = (self.ab_carbon_per_kwh/self.uk_carbon_per_kwh)
			return self.carbon_per_mile_uk *  miles_per_km * carbon_from_electricity_conversion_factor 
	def average_carbon_per_minute(self, minutes_on_bus, minutes_on_train, minutes_waiting, bus_km_per_hour=None, train_km_per_hour=None):
		minutes_per_hour = 60
		if bus_km_per_hour == None:
			bus_km_per_hour = self.bus_km_per_hour
		if train_km_per_hour == None:
			train_km_per_hour = self.train_km_per_hour
		bus_carbon = carbon_per_km(bus=True) * bus_km_per_hour * (minutes_on_bus/minutes_per_hour)
		train_carbon = carbon_per_km(bus=False)* train_km_per_hour * (minutes_on_train/minutes_per_hour)
		return (bus_carbon + train_carbon) / (minutes_on_bus + minutes_on_train + minutes_waiting) 

	def average_cost_per_km(self,  cost_per_fare=2.65, monthly_pass_cost=91.25,
											minutes_on_bus_per_journey, minutes_on_train_per_journey, journeys_per_month,
											bus_km_per_hour=None,train_km_per_hour=None):
		minutes_per_hour = 60
		monthly_pass_cost_per_journey = monthly_pass_cost/journeys_per_month 

		if bus_km_per_hour == None:
			bus_km_per_hour = self.bus_km_per_hour
		if train_km_per_hour == None:
			train_km_per_hour = self.train_km_per_hour

		if monthly_pass_cost_per_journey < cost_per_fare:
			cost_per_journey = monthly_pass_cost_per_journey
		else:
			cost_per_journey = cost_per_fare

		distance_on_bus = minutes_on_bus_per_journey/minutes_per_hour * bus_km_per_hour
		distance_on_train = minutes_on_train_per_journey/minutes_per_hour * train_km_per_hour
		return cost_per_journey / (distance_on_bus + distance_on_train)
	def average_cost_per_minute(self,  cost_per_fare=2.65, monthly_pass_cost=91.25,
													minutes_on_bus_per_journey, minutes_on_train_per_journey, minutes_of_waiting, journeys_per_month,
													bus_km_per_hour=None,train_km_per_hour=None):
		if bus_km_per_hour == None:
			bus_km_per_hour = self.bus_km_per_hour
		if train_km_per_hour == None:
			train_km_per_hour = self.train_km_per_hour
		total_time = minutes_on_bus + minutes_on_train + minutes_of_waiting

		if monthly_pass_cost_per_journey < cost_per_fare:
			cost_per_journey = monthly_pass_cost_per_journey
		else:
			cost_per_journey = cost_per_fare
		return cost_per_journey/(minutes_on_bus_per_journey + minutes_on_train + minutes_of_waiting)
	def total_impact_per_month(self, minutes_on_bus_per_journey, minutes_on_train_per_journey, minutes_of_waiting_per_journey,
							journeys_per_month, bus_km_per_hour=None,train_km_per_hour=None,
							cost_per_fare=2.65,monthly_pass_cost=91.25):
		time_spent_on_transit = journeys_per_month * (minutes_on_bus_per_journey + minutes_on_train_per_journey + minutes_of_waiting_per_journey)
		average_carbon_per_minute = self.average_carbon_per_minute(bus_km_per_hour, train_km_per_hour, minutes_on_bus, minutes_on_train, minutes_waiting)
		average_cost_per_minute = self.average_cost_per_minute(cost_per_fare, monthly_pass_cost,
													minutes_on_bus_per_journey, minutes_on_train_per_journey, minutes_of_waiting, journeys_per_month,
													bus_km_per_hour, train_km_per_hour)
		carbon = average_carbon_per_minute * time_spent_on_transit
		cost = average_dollars_per_minute * time_spent_on_transit
		return (carbon, cost, time_spent_driving, average_carbon_per_minute, average_dollars_per_minute)

class Bicycle():
	km_per_hour = 15.5
	calories_per_day = 1978
	calories_per_km = 50 * 0.621 # 31.5
	fixed_cost_summer_bike = 500
	fixed_cost_winter_bike = 1000
	journey_time = models.IntegerField("When you ride the bike, how many minutes is a typical journey?")
	spring_journeys = models.IntegerField("How many journeys do you take on your bike in a typical week from April to May?")
	summer_journeys = models.IntegerField("How many journeys do you take on your bike in a typical week from June to August?")
	autumn_journeys = models.IntegerField("How many journeys do you take on your bike in a typical week from September to October?")
	winter_journeys = models.IntegerField("How many journeys do you take on your bike in a typical week from November to March?")
	def carbon_per_calorie(self, diet_type, average_calories_per_day=1978):
		days_per_year = 365
		food_carbon_per_year = carbon_footprint[str(diet_type)]
		return food_carbon_per_year/(calories_per_day * days_per_year)
	def carbon_per_km(self, calories_per_km=None): # needs to be converted to minutes
		if calories_per_km == None:
			calories_per_km = self.calories_per_km
		return calories_per_km * carbon_per_calorie(diet_type)
	def carbon_per_minute(self, km_per_hour=None, calories_per_km=None):
			if km_per_hour == None:
				km_per_hour = self.km_per_hour
			return carbon_per_km(calories_per_km) * km_per_hour/60
	def cost_per_km(self, monthly_food_expenses=300, calories_per_day=None, calories_per_km=None, losing_weight=False):
		if losing_weight == True:
			return 0
		else:
			if calories_per_day == None:
				calories_per_day = self.calories_per_day
			if calories_per_km == None:
				calories_per_km = self.calories_per_km
			calories_per_month = calories_per_day * 30 
			cost_per_calorie = monthly_food_expenses / calories_per_month
			return cost_per_calorie * calories_per_km
	def cost_per_minute(self, monthly_food_expenses=300, calories_per_day=None, calories_per_km=None, km_per_hour = None):
		if km_per_hour == None:
			km_per_hour = self.km_per_hour
		return cost_per_km(monthly_food_expenses, calories_per_day, calories_per_km) * (km_per_hour/60) 
	def total_impact(self, minutes_on_bike, monthly_food_expenses=300, calories_per_day=None, calories_per_km=None, km_per_hour = None):
		carbon = average_carbon_per_minute * minutes_on_bike
		cost = cost_per_minute * minutes_on_bike
		return (carbon, cost, minutes_on_bike, average_carbon_per_minute, average_dollars_per_minute)

class Commute(Questions):
	vehicle_used = CharField("Which automobile do you use to commute?", choices =[queryset(Vehicles, filter = request.users), 'Ridesharing'], None)
	minutes_on_freeway = IntegerField("On average, how many minutes do you spend driving at freeway speeds (>80 km/h) during a one-way commute?")
	minutes_in_city = IntegerField("On average, how many minutes do you spend driving at city speeds (<80 km/h) during a one-way commute?")
	minutes_on_train =IntegerField("On average, how many minutes do you spend on the train during a one-way commute?")
	minutes_on_bus = IntegerField("On average, how many minutes do you spend bussing during a one-way commute?")
	minutes_on_bike = IntegerField("On average, how many minutes do you spend biking during a one-way commute?")
	days_of_commute_per_week = IntegerField("On average, how many days do you commute per week?")
	carpooling_passengers = IntegerField("On average, how many carpool passengers are there in a one-way commute?", helptext="enter 0 if you don't drive")
	# percentage_of_year = IntegerField("What percentage of your total commutes does this profile characterize?")

	def carbon_per_commute(Bike, Transit, Vehicle, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city):
		bike_carbon = Bike.carbon_per_minute() * minutes_on_bike
		transit_carbon = Transit.average_carbon_per_minute(minutes_on_bus, minutes_on_train, minutes_of_waiting) * (minutes_on_bus + minutes_on_train + minutes_waiting)
		if vehicle_used == None:
			vehicle_carbon = 0 
		else:
			vehicle_carbon = Vehicle.average_carbon_per_minute(minutes_on_freeway, minutes_in_city)
		return sum(bike_carbon, transit_carbon, vehicle_carbon)
	def cost_per_commute(Bike, Transit, Vehicle, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city, transit_journeys_per_month):
		bike_cost = Bike.cost_per_minute() * minutes_on_bike
		transit_cost = Transit.average_cost_per_minute(minutes_on_bus, minutes_on_train, minutes_of_waiting, transit_journeys_per_month) * (minutes_on_bus + minutes_on_train + minutes_waiting)
		vehicle_cost = Vehicle.average_cost_per_minute(minutes_on_freeway, minutes_in_city)
		return sum(bike_carbon, transit_carbon, vehicle_carbon)
	def time_per_commute(minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city):
		return sum(minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city)

	def carbon_per_month(Bike, Transit, Vehicle, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city, commutes_per_month):
		return  commutes_per_month * cost_per_commute(Bike, Transit, Vehicle, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city, transit_journeys_per_month)

	def cost_per_month(Bike, Transit, Vehicle, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city, commutes_per_month):
		return commutes_per_month * cost_per_commute(Bike, Transit, Vehicle, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city, transit_journeys_per_month)

	def minutes_per_commute(minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city)	:
		return sum(minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city)

	def minutes_commuting_per_month(minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city, commutes_per_week):
		return 4.35 * commutes_per_week * minutes_per_commute(minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city)

 
class ErrandsAndLeisure(Questions):
	vehicle_used = CharField("Which vehicle do you typically use for errands and leisure activites?", choices =[queryset(Vehicles, filter = request.users), 'Ridesharing'], None)
	minutes_on_freeway = IntegerField("On average, how many minutes do you spend driving at freeway speeds (>80 km/h) for errands and leisure activites?")
	minutes_in_city = IntegerField("On average, how many minutes do you spend driving at city speeds (<80 km/h) for errands and leisure activites?")
	minutes_on_train =IntegerField("On average, how many minutes do you spend on the train for errands and leisure activites?")
	minutes_on_bus = IntegerField("On average, how many minutes do you spend bussing for errands and leisure activites?")
	minutes_on_bike = IntegerField("On average, how many minutes do you spend biking for errands and leisure activites?")
	carpooling_passengers = IntegerField("On average, how many carpool passengers are when you go for errands or leisure activities?", helptext="decimals are allowed")

	def carbon_per_month(Bike, Transit, Vehicle, Commute):
		return_carbon_per_month
		bike_carbon = Bike.carbon_per_minute() * minutes_on_bike
		transit_carbon = Transit.average_carbon_per_minute(self.minutes_on_bus, self.minutes_on_train, self.minutes_of_waiting) * (Transit.minutes_on_bus + Transit.minutes_on_train + Transit.minutes_of_waiting)
		if vehicle_used = None:
			vehicle_carbon = 0 
		else:
			vehicle_carbon = Vehicle.average_carbon_per_minute(self.minutes_on_freeway, self.minutes_in_city)
		return sum(bike_carbon, transit_carbon, vehicle_carbon)
	def cost_per_commute(Bike, Transit, Vehicle, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city, transit_journeys_per_month):
		bike_cost = Bike.cost_per_minute() * minutes_on_bike
		transit_cost = Transit.average_cost_per_minute(minutes_on_bus, minutes_on_train, minutes_of_waiting, transit_journeys_per_month) * (minutes_on_bus + minutes_on_train + minutes_waiting)
		vehicle_cost = Vehicle.average_cost_per_minute(minutes_on_freeway, minutes_in_city)
		return sum(bike_carbon, transit_carbon, vehicle_carbon)

	def carbon_per_month(Bike, Transit, Vehicle, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city, commutes_per_month):
		return  commutes_per_month * cost_per_commute(Bike, Transit, Vehicle, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city, transit_journeys_per_month)

	def cost_per_month(Bike, Transit, Vehicle, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city, commutes_per_month):
		return commutes_per_month * cost_per_commute(Bike, Transit, Vehicle, minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city, transit_journeys_per_month)

	def minutes_per_commute(minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city)	:
		return sum(minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city)

	def minutes_commuting_per_month(minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city, commutes_per_week):
		return 4.35 * commutes_per_week * minutes_per_commute(minutes_of_biking, minutes_on_bus, minutes_on_train, minutes_of_waiting, minutes_on_freeway, minutes_in_city)


class Vacation(Questions):
	method = CharField( choices = [queryset(Vehicles, filter = request.users), 'Flight', 'Train', 'Bus'], )
	destination = CharField('Where did you go?')
	hours_one_way = FloatField('What was the one-way travel time required to get to this destination?' helptext = 'exclude time spent stopped, resting, or laying over')
	round_trip = BooleanField('Was this a round trip?')

	def vacation_trnsportation_carbon(self, method, km_per_hour = 100,):
		if method == 'flight':
			carbon_per_hour =  carbon_footprint['hour of flight']
		elif method == 'train':
			carbon_per_hour=  carbon_footprint['minute on train'] * 60
		elif method == 'bus':
			carbon_per_hour = carbon_footprint['minute on bus'] * 60
		else:
			carbon_per_hour = km_per_hour * self.vehicle_used.carbon_per_km(city=False)
		if self.round_trip:
			return carbon_per_hour * self.hours_one_way * 2 # 2 to account for round trip
		else:
			return carbon_per_hour * self.hours_one_way


class TransportationStrategy(Strategy):

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
	
	#divide according to work, vacations, and chores/leisure
	def adjust_share_of_transportation(litres_per_hundred_km, fuel_type, avg_non_household_passengers, transit_type, percent_shifted, yearly_km_travelled):
		change_in_emissions_per_km = litres_per_hundred_km * carbon_footprint[fuel_type]/avg_non_household_passengers *100 - carbon_footprint[transit_type]
		return change_in_emissions_per_km * percent_shifted * yearly_km_travelled




class VehicleStrategy(TransportationStrategy):
	def litres_per_hundred_km_avg(distance_driven_city, distance_driven_freeway, litres_per_hundred_km_freeway, litres_per_hundred_km_city):
		return (distance_driven_city * litres_per_hundred_km_city + distance_driven_freeway * litres_per_hundred_km_freeway)/ (distance_driven_city + distance_driven_freeway)

	def yearly_distance_driven(litres_per_tank, fuel_ups_per_month, litres_per_hundred_km_avg):
		return litres_per_tank * fuel_ups_per_month / litres_per_hundred_km_avg

	def swap_to_electric_car(litres_per_hundred_km_avg, fuel_type, kwh_per_hundred_km_avg, yearly_distance_driven, percent_renewable_gen):
		emissions_per_km_vehicle_one = carbon_footprint['fuel_type'] * litres_per_hundred_km_avg * 100 
		emissions_per_km_vehicle_two = carbon_footprint['electricity'] *(1-percent_renewable_gen) * kwh_per_hundred_km_avg * 100
		return (emissions_per_km_vehicle_one - emissions_per_km_vehicle_two) * yearly_distance_driven

	def increase_fuel_efficiency(yearly_distance_driven, fuel_type):
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
	
	def add_person_to_carpool(litres_per_hundred_km_passenger_vehicle, fuel_type, preexisting_passengers):
		km_commuted_per_month = (distance_to_work + distance_to_passenger) * shifts_per_week * 2
		passenger_emissions_from_driving_avoided = km_commuted_per_month * litres_per_hundred_km *100 * carbon_footprint[fuel_type] 
		return passenger_emissions_from_driving_avoided / 2 # divide by 2 splits emission reductions evenly between passenger and driver

	

	
class RideshareStrategy(TransportationStrategy):
	def adjust_share_of_transportation(litres_per_hundred_km, fuel_type, avg_non_household_passengers, transit_type, percent_shifted, yearly_km_travelled):
		change_in_emissions_per_km = litres_per_hundred_km * carbon_footprint[fuel_type]/avg_non_household_passengers *100 - carbon_footprint[transit_type]
		return change_in_emissions_per_km * percent_shifted * yearly_km_travelled
	
	
class TransitStrategy(TransportationStrategy):
	def bike_to_work(months_per_year, distance_to_work, shifts_per_week, fuel_type, gas_mileage, diet, calories_per_year):
		km_commuted_per_month = distance_to_work * shifts_per_week * 2
		emissions_from_driving = km_commuted_per_month * litres_per_hundred_km *100 * carbon_footprint[fuel_type] 
		carbon_per_calorie = carbon_footprint[diet]/calories_per_year
		emissions_from_biking = distance_to_work * calories_burned * carbon_per_calorie *2
		return emissions_from_driving - emissions_from_biking
	

class FlightStrategy(Strategy):
	def one_fewer_flight(length_of_flight):
		return length_of_flight * carbon_footprint['flight']

	def one_hour_less_flight():
		return carbon_footprint['flight']

	def one_less_vacation(distance_to_destination, avg_light_passenger_vehicle_litres_per_hundred_km):
		#Rests on the assumptiont that emissions from flying are about as much as emissions from driving per kilometer 
		return distance_to_destination *carbon_footprint['gasoline'] * avg_light_passenger_vehicle_litres_per_hundred_km * 100 *  2
	
	def reduce_distance_to_vacation(fuel_type, litres_per_hundred_km_freeway, change_in_distance):
		return carbon_footprint[fuel_type] * litres_per_hundred_km_freeway * change_in_distance

class BicycleStrategy(TransportationStrategy):
	pass

# class DailyTransport(Questions):
# 	class Meta:
# 		abstract=True

# 	def per_week_modifier(self, commutes_per_day=2):
# 		return self.days_of_commute_per_week * commutes_per_day

# 	def km_travelled_bicycle(self, average_km_per_hour=15.5, travel_time=self.minutes_of_biking):
# 		return travel_time * average_km_per_hour / 60
# 	def km_travelled_bus(self, average_km_per_hour=19.5, travel_time=self.minutes_of_bussing):
# 		return travel_time * average_km_per_hour / 60
# 	def km_travelled_train(self, average_km_per_hour=30, travel_time=self.minutes_of_light_rail_transit):
# 		return travel_time * average_km_per_hour / 60
# 	def km_travelled_car_city(self, average_km_per_hour=38, travel_time=self.minutes_of_city_driving):
# 		return travel_time * average_km_per_hour  / 60
# 	def km_travelled_car_freeway(self, average_km_per_hour=100, travel_time=self.minutes_of_freeway_driving):
# 		return travel_time * average_km_per_hour / 60
# 	def total_km_travelled(self):
# 		return sum(km_travelled_car_freeway(), km_travelled_car_city(), km_travelled_train(), km_travelled_bus(), km_travelled_bicycle())


	
# 	def bicycle_footprint_per_week(self, calories_per_mile=50, calories_per_day=1978, bike_km_per_hour=15.5, travel_time=self.minutes_of_biking): 
# 		miles_per_km,  days_per_year, = 0.62, 60, 365.25
# 		food_carbon_per_year = self.user.food.footprint()
# 		carbon_per_calorie = food_carbon_per_year / (calories_per_day * days_per_year)
# 		calories_per_km = calories_per_mile * miles_per_km
# 		carbon_per_km = carbon_per_calorie * calories_per_km
# 		return carbon_per_km * self.km_travelled_bicycle(bike_km_per_hour, travel_time) * self.per_week_modifier()

# 	def freeway_footprint_per_week(self, average_km_per_hour_freeway = 100, travel_time = self.minutes_of_freeway_drivings):
# 		km_driven_freeway = self.km_travelled_car_freeway(average_km_per_hour_freeway, travel_time) * self.per_week_modifier()
# 		return (km_driven_freeway * self.vehicle_used.carbon_per_km(city=False)) / self.carpooling_passengers

# 	def city_driving_footprint_per_week(self, average_km_per_hour_city = 38, travel_time = self.minutes_of_city_driving):
# 		km_driven_city = self.km_travelled_car_city(average_km_per_hour_city, travel_time) * self.per_week_modifier()
# 		return (km_driven_city * self.vehicle_used.carbon_per_km(city=True)) / self.carpooling_passengers

# 	def train_footprint_per_week(self, carbon_per_mile_uk=0.19, uk_carbon_per_kwh=0.49, ab_carbon_per_kwh=0.90, km_per_hour=30, travel_time = self.minutes_of_light_rail_transit):
# 		miles_per_km = 0.62
# 		carbon_per_km = carbon_per_mile_uk * (ab_carbon_per_kwh/uk_carbon_per_kwh) * miles_per_km
# 		return carbon_per_km *  self.km_travelled_train(km_per_hour_train=30, travel_time=self.minutes_of_light_rail_transit) * self.per_week_modifier()

# 	def bus_footprint_per_week(self, carbon_per_mile = 0.15, km_per_hour_bus=12.1, travel_time = self.minutes_of_bussing):
# 		miles_per_km =0.62
# 		carbon_per_km = carbon_per_mile * miles_per_km
# 		return carbon_per_km *  self.km_travelled_bus_per_commute(km_per_hour_bus, travel_time) * self.per_week_modifier()

# 	def switch_transit_method(self, initial_method, replacement_method, initial_method_speed, replacement_method_speed):
		
# 		methods = {
# 			'bike': [km_travelled_bicycle, bicycle_footprint_per_week, self.minutes_of_biking],
# 			'bus': [km_travelled_bus, bicycle_footprint_per_week, self.minutes_of_bussing],
# 			'light_rail_transit': [km_travelled_train, bicycle_footprint_per_week, self.minutes_of_light_rail_transit],
# 			'city_driving': [km_travelled_car_city, bicycle_footprint_per_week, self.minutes_of_city_driving],
# 			'freeway_driving': [km_travelled_car_freeway, freeway_footprint_per_week, self.minutes_of_freeway_driving]
# 		}
# 		old_footprint = methods[initial_method][1]() + methods[replacement_method][1]()
# 		original_replacement_method_time = 
# 		extra_travel_time = methods[initial_method][0]() / replacement_method_speed
# 		new footprint = methods[replacement_method][1](travel_time = (original_replacement_method_time + extra_travel_time))
# 		carbon_savings = old_footprint - new_footprint()
# 		time_cost = extra_travel_time
# 		financial_cost = 
# 		time 
