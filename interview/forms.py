from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Survey, Food, Transportation, Vehicle 
from .models import Rideshare, Flight, Transit, Bicycle
from .models import  Household, Appliances, Trash, NaturalGas, Electricity
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class SurveyForm(ModelForm):
	class Meta:
		model = Survey
		fields = ('electricity', 'natgas', 'gasoline',)

class SignUpForm(ModelForm):
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password',)

class TransportationForm(ModelForm):
	class Meta:
		model = Transportation
		fields = ('vehicles_owned', 'flights_taken', 'use_rideshare', 'ride_public_transit', 'own_summer_bike', 'own_winter_bike',
					   'distance_to_work')

class VehicleForm(ModelForm):
	class Meta:
		model = Vehicle
		fields = ('fuel_type', 'fuel_ups', 'tank_size', 'fuel_economy_city', 'fuel_economy_highway',
					  'km_driven_city', 'km_driven_highway', 'vehicle_cost', 'fuel_cost' ) #add 'fuel_economy_city

class RideshareForm(ModelForm):
	class Meta:
		model = Rideshare
		fields = ('journeys', 'journey_time', 'cost')

class FlightForm(ModelForm):
	class Meta:
		model = Flight
		fields = ('length', 'round_trip',  'cost')

class TransitForm(ModelForm):
	class Meta:
		model = Transit
		fields = ('train_journeys', 'train_journey_time', 'bus_journeys', 'bus_journey_time', 'cost')

class BicycleForm(ModelForm):
	class Meta:
		model = Bicycle
		fields = ('journey_time', 'spring_journeys' ,'summer_journeys', 'autumn_journeys', 'winter_journeys')

class HouseholdForm(ModelForm):
	class Meta:
		model = Household
		fields = ('utilities_included', 'electricity_bills', 'renewable_energy_share', 'gas_bills', 'biogas_share', 'residents',
					  'size', 'housing_cost', 'able_to_move', 'building_type', 'owernship_type' )

class AppliancesForm(ModelForm):
	class Meta:
		model = Appliances
		fields = ('appliances_in_residence', 'high_efficiency_appliances')

class TrashForm(ModelForm):
	class Meta:
		model = Trash
		fields = ('garbage_bin_volume', 'garbage_bin_fill_time')

class NaturalGasForm(ModelForm):
	class Meta:
		model = NaturalGas
		fields = ('january_natural_gas', 'february_natural_gas', 'march_natural_gas', 'april_natural_gas', 'may_natural_gas', 'june_natural_gas',
		 			  'july_natural_gas', 'august_natural_gas', 'september_natural_gas', 'october_natural_gas', 'november_natural_gas', 'december_natural_gas',
					  'january_cost', 'february_cost', 'march_cost', 'april_cost', 'may_cost', 'june_cost',
		 			  'july_cost', 'august_cost', 'september_cost', 'october_cost', 'november_cost', 'december_cost', )

class ElectricityForm(ModelForm):
	class Meta:
		model = Electricity
		fields = ('january_electricity', 'february_electricity', 'march_electricity', 'april_electricity', 'may_electricity', 'june_electricity',
		 			  'july_electricity', 'august_electricity', 'september_electricity', 'october_electricity', 'november_electricity', 'december_electricity',
					  'january_cost', 'february_cost', 'march_cost', 'april_cost', 'may_cost', 'june_cost',
		 			  'july_cost', 'august_cost', 'september_cost', 'october_cost', 'november_cost', 'december_cost', )

class FoodForm(ModelForm):
	class Meta:
		model = Food
		fields = ('diet', 'food_intake', 'local_share', 'seasonal', 'grocery_cost', 'restaurant_cost')
