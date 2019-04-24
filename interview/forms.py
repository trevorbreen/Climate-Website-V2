from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import  Profile, Food, Vehicle 
from .models import Rideshare, Flight, Transit, Bicycle
from .models import  Residence, Trash, NaturalGas, Electricity
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


all_models = {
	"profile": Profile,
	"vehicle": Vehicle,
	"rideshare": Rideshare,
	"flight": Flight,
	"transit": Transit,
	"bicycle": Bicycle,
	"residence": Residence,
	#"appliances": Appliances,
	"trash": Trash,
	"natural_gas": NaturalGas,
	"electricity": Electricity,
	"food": Food,
	}

	
all_formsets = {
	"profile": modelformset_factory(Profile, exclude=('user',), extra=1, max_num = 1),
	"vehicle": modelformset_factory(Vehicle, exclude=('user',)),
	"rideshare": modelformset_factory(Rideshare, exclude=('user',), max_num = 1),
	"flight": modelformset_factory(Flight, exclude=('user',)),
	"transit": modelformset_factory(Transit, exclude=('user',), max_num = 1),
	"bicycle": modelformset_factory(Bicycle, exclude=('user',), max_num = 1),
	"residence": modelformset_factory(Residence, exclude=('user',), max_num = 1),
#	"appliances": modelformset_factory(Appliances, exclude=('user',), max_num = 1),
	"trash": modelformset_factory(Trash, exclude=('user',), max_num = 1),
	"natural_gas": modelformset_factory(NaturalGas, exclude=('user',), max_num = 1),
	"electricity": modelformset_factory(Electricity, exclude=('user',), max_num = 1),
	"food": modelformset_factory(Food, exclude=('user',), max_num = 1),
	}
