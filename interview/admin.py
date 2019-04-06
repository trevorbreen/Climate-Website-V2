# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Profile, Bicycle, Vehicle, Flight, Rideshare, Transit, Food, Residence, Electricity, NaturalGas, Trash, Appliances

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username']

admin.site.register(CustomUser)
#admin.site.register(CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Bicycle)
admin.site.register(Vehicle)
admin.site.register(Flight)
admin.site.register(Rideshare)
admin.site.register(Transit)
admin.site.register(Food)
admin.site.register(Residence)
admin.site.register(Electricity)
admin.site.register(NaturalGas)
admin.site.register(Trash)
admin.site.register(Appliances)
