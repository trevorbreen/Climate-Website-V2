#Parameters 
carbon_footprint ={
'kwh of electricity'  :  0.9,
'litre of gasoline' : 2.71, #Assuming gas is produced in Alberta
'litre of diesel' : 3.19,
'GJ natural gas' : 57.08, # 0.002129 kg/l * 1000 l/m^3 * 26.853 m^3/GJ
'hour of flight' : 250.00, # Carbon Independent Methodology
'omnivore diet' : 2500,
'no beef diet' : 1900,
'vegetarian diet' : 1700, 
'vegan diet' :1500,
'kg of beef' : 31.42,
'kg of pork' : 4.11,
'kg of chicken' : 1.79,
'L of milk' : 0.92,
'kg of cheese' : 7.36,
'dozen eggs' : 1.78,
'litre of trash' : 0.23,
'minute on bus': 0.030,
'minute on train': 0.108,
'minute on bicycle' : 0.02,
'one dollar in alberta' : 0.834,
'one dollar in canada'  : 0.346,
'kg of trash' : 0.5,
}

#avg_bike_speed = 

#calories_per_km_bike = 

#avg_fuel_economy_car_canada =

#emissions_per_minute_bus = 70 000 tonnes CO2e from busses, 30 000 tonnes CO2e from LRT (total 2014)

#emissions_per_minute_train = 


#Parameters we need to fetch 
#Avg Vehicle Speed, avg vehicle milage, avg vehicle fuel economy ()

#Train distance
#190 g/mile how bad are bananas (UK)
# uk carbon intensity of electricity =   0.46219 +  0.03816  = 0.49 kgco2e/kwh
#can caluculate new emission factor for alberta 
# 17.2 miles per hour https://www.lightrailnow.org/myths/m_lrt012.htm
# edmonton avg speed (km/h) = 76*33 + 34*24 / 110 from ETS ridership
# lrt speed = 30 km/h


#Bus
# 150 g/mile How bad is a banana
# 12.1 miles per hour APTA https://www.apta.com/resources/statistics/Documents/FactBook/2017-APTA-Fact-Book.pdf

# 1.609 km/mile 

#Bicycle
# 50 calories per mile how bad are bananas

# 1978 calories per day statscanada https://www150.statcan.gc.ca/n1/daily-quotidien/170620/dq170620b-eng.htm
# 365.25 days per year
# Diet input by user 

#RideShare
# 22.4 miles per gallon how bad are bananas
# 25 mph lightrailnow


#Trash
# 0.5 kg co2e per kg garbage how bad are bananas
# 95 lbs per cubic yard EPA https://www.epa.gov/sites/production/files/2016-04/documents/volume_to_weight_conversion_factors_memorandum_04192016_508fnl.pdf
#764.5 litres per cubic yard
# 2.2 pounds per kilogram
def trash_footprint(carbon_per_kg=0.5, pounds_per_cubic_yard=764.5):
	litres_per_cubic_yard = 764.5
	kilograms_per_pound = 1/2.2
	return carbon_per_kg * (pounds_per_cubic_yard *kilograms_per_pound)/ litres_per_cubic_yard

def bus_footprint(carbon_per_mile = 0.15, miles_per_hour=12.1):
	minutes_per_hour = 60
	return carbon_per_mile * miles_per_hour / minutes_per_hour

def train_footprint(carbon_per_mile_uk=0.19, uk_carbon_per_kwh=0.49, ab_carbon_per_kwh=0.90, km_per_hour=30):
	miles_per_hour = km_per_hour/1.609
	minutes_per_hour = 60
	return (carbon_per_mile_uk * (ab_carbon_per_kwh/uk_carbon_per_kwh) * miles_per_hour) / minutes_per_hour

def cycling_footprint(calories_per_mile, calories_per_day, food_carbon_per_year, bike_km_per_hour): # needs to be converted to minutes
	miles_per_km = 0.621
	minutes_per_hour = 60
	calories_per_minute = calories_per_mile * miles_per_km * bike_km_per_hour / minutes_per_hour
	calories_per_year = calories_per_day * 365.25
	carbon_per_calorie = food_carbon_per_year / calories_per_year
	return carbon_per_calorie * calories_per_minute
