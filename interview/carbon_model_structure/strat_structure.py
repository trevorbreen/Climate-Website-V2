from .parameters import carbon_footprint
def total_carbon(residential_carbon, transportation_carbon, consumption_carbon, savings_carbon, food_carbon):

	def transportation_carbon(commute_carbon, out_of_town_carbon, errands_and_shopping_carbon, leisure_carbon):
		def purpose_carbon(flight_carbon, vehicle_carbon, transit_carbon, bicycle_carbon):
			def flight_carbon():
				pass
			def vehicle_carbon():
				pass
			def transit_carbon():
				pass
			def bicycle_carbon():
				pass
			return sum(flight_carbon, vehicle_carbon, transit_carbon, bicycle_carbon)
		return sum(commute_carbon, out_of_town_carbon, errands_and_shopping_carbon, leisure_carbon)


	def residential_carbon(electricity_carbon, natural_gas_carbon, trash_carbon, building_carbon, water_carbon):
		def electricty_carbon(appliance_carbon, lights_carbon, ):
			pass
		def natural_gas_carbon():
			pass
		def trash_carbon():
			pass
		def building_carbon():
			pass
		def water_carbon():
			pass

		return sum(electricity_carbon, natural_gas_carbon, trash_carbon, building_carbon, water_carbon)

	return(sum(residential_carbon, transportation_carbon, consumption_carbon, savings_carbon, food_carbon))



from .parameters import carbon_footprint


def transportation(commute, out_of_town, errands_and_shopping, leisure):
	def purpose(flight, vehicle, transit, bicycle):
		def flight():
			pass
		def vehicle():
			pass
		def transit():
			pass
		def bicycle():
			pass
		return sum(flight, vehicle, transit, bicycle)
	return sum(commute, out_of_town, errands_and_shopping, leisure)


def residential(electricity, natural_gas, trash, building, water):
	def electricty():
		pass
	def natural_gas():
		pass
	def trash():
		pass
	def building():
		pass
	def water():
		pass
	return sum(electricity, natural_gas, trash, building, water)

def food(meat, dairy, eggs, plan_protien, fruits_and_vegtables, oils, starch_and_carbs, desert):
	def meat():
		pass
	def dairy():
		pass
	def eggs():
		pass
	def plant_protien():
		pass
	def fruits_and_vegtables():
		pass
	def oils():
		pass
	def starch_and_carbs():
		pass
	def desert():
		pass
	return sum(meat, dairy, eggs, plan_protien, fruits_and_vegtables, oils, starch_and_carbs, desert)

def savings(cash, bonds, stocks, real_estate, mutual_funds):
	def cash():
		pass
	def bonds():
		pass
	def stocks():
		pass
	def real_estate():
		pass
	def mutual_funds():
		pass
	return sum(cash, bonds, stocks, real_estate, mutual_funds)

def consumption(furniture, clothing, recreation, electronics, other):
	def furniture():
		pass
	def clothing():
		pass
	def recreation():
		pass
	def electronics():
		pass
	def other():
		pass
	return sum(furniture, clothing, recreation, electronics, other)

def total(residential, transportation, consumption, savings, food):
	return(sum(residential, transportation, consumption, savings, food))







