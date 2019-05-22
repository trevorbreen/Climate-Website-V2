from parameters import carbon_footprint


# return GJ of nat gas consumed per month? You can also multiply by carbon_footprint['GJ natural gas'] to get co2e/month
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




def increase_fuel_efficiency(yearly_distance_driven, fuel_type, old_litres_per_hundred_km, new_litres_per_hundred_km):
	increase_in_efficiency_per_km = (old_litres_per_hundred_km - new_litres_per_hundred_km) * 100
	return increase_in_efficiency_per_km * carbon_footprint[fuel_type] *  yearly_distance_driven  
