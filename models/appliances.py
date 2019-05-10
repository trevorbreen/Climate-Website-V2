
class HighEfficiencyStandardAppliance(models.Model):
	class Meta:
		abstract = True

	def __init__(self, use, active_install_time, active_time_per_use, fixed_cost, fixed_carbon,
			electricity_per_use, natural_gas_per_use, water_per_use, lifetime):
		self.use = str(use)
		self.active_install_time = active_install_time
		self.active_time_per_use = active_time_per_use 
		self.fixed_cost = fixed_cost
		self.fixed_carbon = fixed_carbon 
		self.high_efficiency = True
		self.electricity_per_use = float(electricity_per_use)
		self.natural_gas_per_use = float(natural_gas_per_use)
		self.water_per_use = float(water_per_use) 
		self.lifetime = lifetime
		
	def electricity_cost(self, uses_per_week, cost_per_kwh):
		return uses_per_week * self.electricity_per_use * carbon_per_kwh 	
	def natural_gas_cost(self, uses_per_week, cost_per_GJ):
		return uses_per_week * self.natural_gas_per_use * carbon_per_GJ
	def water_cost(self, uses_per_week, cost_per_cubic_metre):
		return uses_per_week * self.natural_gas_per_use * carbon_per_cubic_metre
	def cost_per_week(self, uses_per_week, cost_per_kwh, cost_per_GJ, cost_per_cubic_metre):
		return sum(self.electricty_cost(uses_per_week, cost_per_kwh), self.natural_gas_cost(uses_per_week, cost_per_GJ), self.water_cost(uses_per_week, cost_per_cubic_metre))
	
	def electricity_carbon(self, uses_per_week, carbon_per_kwh):
		return uses_per_week * self.electricity_per_use * carbon_per_kwh 	
	def natural_gas_carbon(self, uses_per_week, carbon_per_GJ):
		return uses_per_week * self.natural_gas_per_use * carbon_per_GJ
	def water_carbon(self, uses_per_week, carbon_per_cubic_metre):
		return uses_per_week * self.natural_gas_per_use * carbon_per_cubic_metre	
	def carbon_per_week(self, uses_per_week, carbon_per_kwh, carbon_per_GJ, carbon_per_cubic_metre):
		return sum(self.electricty_footprint(uses_per_week, carbon_per_kwh), self.natural_gas_footprint(uses_per_week, carbon_per_GJ), self.water_footprint(uses_per_week, carbon_per_cubic_metre))

	def time_per_week(self, uses_per_week):
		return uses_per_week * self.active_time_per_use

	
class Appliance(HighEfficiencyStandardAppliance):
	class Meta:
		abstract = True
	def __init__(self, uses_per_week, high_efficiency= False, electricity_per_use, natural_gas_per_use, water_per_use, active_time_per_use = HighEfficiencyStandardAppliance.active_time_per_use, age):
		self.uses_per_week = models.FloatField()
		self.high_efficiency = models.BooleanField()
		self.electricity_per_use = models.FloatField()
		self.natural_gas_per_use = models.FloatField()
		self.water_per_use = models.FloatField()
		self.active_time_per_use = models.FloatField()
		self.weeks_remaining = max(self.lifetime - self.age, 1) 

	def upgrade_carbon_savings_per_week(self, carbon_per_kwh, carbon_per_GJ, carbon_per_cubic_metre):
		return self.carbon_per_week(self.uses_per_week,**locals()) - super(Appliance, self).carbon_per_week(self.uses_per_week,**locals()) - self.fixed_carbon/self.weeks_remaining
	def upgrade_cost_per_week(self, cost_per_kwh, cost_per_GJ, cost_per_cubic_metre):
		return self.cost_per_week(self.uses_per_week,**locals()) - super(Appliance, self).cost_per_week(self.uses_per_week,**locals()) - self.fixed_cost/self.weeks_remaining
	def upgrade_time_savings_per_week(self, uses_per_week):
		return self.time_per_week(**locals()) - super(Appliance, self).time_per_week(**locals()) + self.active_install_time/self.weeks_remaining

	def total_upgrade_carbon_savings(self, uses_per_week, carbon_per_kwh, carbon_per_GJ, carbon_per_cubic_metre):
		return self.weeks_remaining * (self.carbon_per_week(self.uses_per_week, carbon_per_kwh, carbon_per_GJ, carbon_per_cubic_metre) - super(Appliance, self).carbon_per_week(**locals())) - self.fixed_carbon
	def total_upgrade_cost(self, uses_per_week, cost_per_kwh, cost_per_GJ, cost_per_cubic_metre):
		return self.weeks_remaining * (self.cost_per_week(self.uses_per_week, cost_per_kwh, cost_per_GJ, cost_per_cubic_metre) - super(Appliance, self).cost_per_week(**locals())) - self.fixed_cost
	def total_upgrade_time_savings(self, uses_per_week):
		return self.weeks_remaining * (self.time_per_week(self.uses_per_week) - super(Appliance, self).time_per_week(**locals())) - self.active_install_time
	
	def use_reduction_outcome(self, use_per_week_reduction, upgrade_to_high_efficiency, carbon_per_kwh, carbon_per_GJ, carbon_per_cubic_metre):
		new_uses_per_week = self.uses_per_week - use_per_week_reduction
		if upgrade_to_high_efficiency:
			reference = super(Appliance, self)
			horizion = self.weeks_remaining # week
			carbon_savings = total_upgrade_carbon_savings(new_uses_per_week, carbon_per_kwh, carbon_per_GJ, carbon_per_cubic_metre)
			cost = self.cost_per_week(new_uses_per_week, cost_per_kwh, cost_per_GJ, cost_per_cubic_metre)
			time_savings = self.time_per_week(new_uses_per_week)
		else:
			reference = self
			horizion = 1 # week	
			carbon_savings = self.carbon_per_week(use_per_week_reduction, carbon_per_kwh, carbon_per_GJ, carbon_per_cubic_metre)
			cost = self.cost_per_week(use_per_week_reduction, cost_per_kwh, cost_per_GJ, cost_per_cubic_metre)
			time_savings = self.time_per_week(use_per_week_reduction)
			carbon_savings_per_dollar = carbon_savings / cost
			carbon_savings_per_time = carbon_savings / time_savings
		return (carbon_savings, cost, time_savings, carbon_savings_per_dollar, carbon_savings_per_time, horizion) 

freezer = HighEfficiencyStandardAppliance('temperature_gradient_per_minute', 240, 0, 1000, fixed_carbon,
																	electricity_per_use, 0, 0, lifetime)

fridge = HighEfficiencyStandardAppliance(use, active_install_time, active_time_per_use, fixed_cost, fixed_carbon,
																	electricity_per_use, natural_gas_per_use, water_per_use, lifetime)

washer = HighEfficiencyStandardAppliance(use, active_install_time, active_time_per_use, fixed_cost, fixed_carbon,
																	electricity_per_use, natural_gas_per_use, water_per_use, lifetime)
dryer = HighEfficiencyStandardAppliance(use, active_install_time, active_time_per_use, fixed_cost, fixed_carbon,
																	electricity_per_use, natural_gas_per_use, water_per_use, lifetime)
stove = HighEfficiencyStandardAppliance(use, active_install_time, active_time_per_use, fixed_cost, fixed_carbon,
																	electricity_per_use, natural_gas_per_use, water_per_use, lifetime)
fridge = HighEfficiencyStandardAppliance(use, active_install_time, active_time_per_use, fixed_cost, fixed_carbon,
																	electricity_per_use, natural_gas_per_use, water_per_use, lifetime)
oven = HighEfficiencyStandardAppliance(use, active_install_time, active_time_per_use, fixed_cost, fixed_carbon,
																	electricity_per_use, natural_gas_per_use, water_per_use, lifetime)
microwave = HighEfficiencyStandardAppliance(use, active_install_time, active_time_per_use, fixed_cost, fixed_carbon,
																	electricity_per_use, natural_gas_per_use, water_per_use, lifetime)
computer = HighEfficiencyStandardAppliance(use, active_install_time, active_time_per_use, fixed_cost, fixed_carbon,
																	electricity_per_use, natural_gas_per_use, water_per_use, lifetime)
television = HighEfficiencyStandardAppliance(use, active_install_time, active_time_per_use, fixed_cost, fixed_carbon,
																	electricity_per_use, natural_gas_per_use, water_per_use, lifetime)
hvac = HighEfficiencyStandardAppliance(use, active_install_time, active_time_per_use, fixed_cost, fixed_carbon,
																	electricity_per_use, natural_gas_per_use, water_per_use, lifetime)
boiler = HighEfficiencyStandardAppliance(use, active_install_time, active_time_per_use, fixed_cost, fixed_carbon,
																	electricity_per_use, natural_gas_per_use, water_per_use, lifetime)
lights = HighEfficiencyStandardAppliance(use, active_install_time, active_time_per_use, fixed_cost, fixed_carbon,
																	electricity_per_use, natural_gas_per_use, water_per_use, lifetime)
shower = HighEfficiencyStandardAppliance(use, active_install_time, active_time_per_use, fixed_cost, fixed_carbon,
																	electricity_per_use, natural_gas_per_use, water_per_use, lifetime)
bathtub = HighEfficiencyStandardAppliance(use, active_install_time, active_time_per_use, fixed_cost, fixed_carbon,
																	electricity_per_use, natural_gas_per_use, water_per_use, lifetime)
furnace = HighEfficiencyStandardAppliance(use, active_install_time, active_time_per_use, fixed_cost, fixed_carbon,
																	electricity_per_use, natural_gas_per_use, water_per_use, lifetime)
# class Appliances(models.Model):
# 	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
# 	present = models.BooleanField('Do you have this appliance in your house?', null=True, blank=True)
# 	efficient = models.BooleanField('Do you already have a high efficiency version of this appliance?', null=True, blank=True)

