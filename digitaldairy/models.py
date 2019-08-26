from django.db import models
from django.urls import reverse
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone_number = models.CharField(max_length=12)
	client_address = models.CharField(max_length=100, blank=True, default='')
	farm_name = models.CharField(max_length=100, blank=True, default='')
	farm_location = models.CharField(max_length=100, blank=True, default='')

	def __str__(self):
		return self.user.username


def create_profile(sender, **kwargs):
	if kwargs['created']:
		UserProfile.objects.create(user=kwargs['instance'])


def save_profile(sender, instance, **kwargs):
	instance.profile.save()


post_save.connect(create_profile, sender=User)
post_save.connect(save_profile, sender=User)


class SemenRecords(models.Model):
	id = models.AutoField(primary_key=True)
	bull_code = models.CharField(max_length=100, db_index=True)
	bull_name = models.CharField(max_length=100, blank=True)
	bull_breed = models.CharField(max_length=100, blank=True, default='')
	num_of_straws = models.DecimalField(max_digits=10, default=0, decimal_places=2)
	cost_per_straw = models.DecimalField(max_digits=10, default=0, decimal_places=2)
	company_name = models.CharField(max_length=100, blank=True, default='')

	def __str__(self):
		return "{0}".format(self.bull_code)

	class Meta:
		db_table = 'semen_records'


class Cow(models.Model):
	id = models.CharField(primary_key=True, max_length=100)
	name = models.CharField(max_length=100)
	lactations = models.IntegerField(null=True, default=0)
	grade = models.CharField(max_length=30, blank=True, default='PEDIGREE', choices=[('PEDIGREE', 'PEDIGREE'), ('APPENDIX', 'APPENDIX'), ('POOL', 'POOL'), ('INTERMEDIATE', 'INTERMEDIATE'), ('FOUNDATION','FOUNDATION')])
	breed = models.CharField(max_length=30, blank=True, default='')
	color = models.CharField(max_length=30, blank=True, default='')
	dob = models.DateField()
	sire = models.ForeignKey(SemenRecords, related_name="cow_sire", null=True, on_delete=models.SET_NULL)
	dam = models.ForeignKey('self', related_name="cow_dam", null=True, on_delete=models.SET_NULL)
	group = models.CharField(max_length=30, blank=True, default='')
	status = models.CharField(max_length=30, blank=True, default='Active')
	birth_weight = models.DecimalField(default=0, null=True, decimal_places=2, max_digits=10)
	category = models.CharField(max_length=30, default="Heifer", choices=[('Milker', 'Milker'), ('Heifer', 'Heifer'), ('Dry', 'Dry'), ('Steamer', 'Steamer'), ('Incalf Heifer', 'Incalf Heifer'), ('Calf', 'Calf'), ( 'Weaner',  'Weaner'), ('Weaner 1', 'Weaner 1'), ('Weaner 2', 'Weaner 2'), ('Weaner 3', 'Weaner 3'), ( 'Yearling',  'Yearling'),('Bulling', 'Bulling'), ('Bull', 'Bull')])
	source = models.CharField(max_length=50, blank=True, default='')

	def get_absolute_url(self):
		return reverse('digitaldairy:cow_profile', args=[self.id], current_app='digitaldairy')

	def milk_production_history_url(self):
		return '/digitaldairy/milk_production_history/?cow_id={0}'.format(self.id)

	def __str__(self):
		return self.id

	class Meta:
		ordering = ['name']
		db_table = 'cow'


class CowBodyTraits(models.Model):
	cow = models.ForeignKey(Cow, primary_key=True, on_delete=models.CASCADE)
	frame = models.DecimalField(decimal_places=2, default=0, max_digits=10)
	dairy_strength = models.DecimalField(decimal_places=2, default=0, max_digits=10)
	udder = models.CharField(max_length=10, blank=True, default='')
	feet_legs = models.CharField(max_length=10, blank=True, default='')
	stature = models.CharField(max_length=10, blank=True, default='')
	chest_width = models.DecimalField(decimal_places=2, default=0, max_digits=10)
	body_depth = models.DecimalField(decimal_places=2, default=0, max_digits=10)
	angularity = models.CharField(max_length=10, blank=True, default='')
	cond_score = models.DecimalField(decimal_places=2, default=0, max_digits=10)
	thurl_width = models.DecimalField(decimal_places=2, default=0, max_digits=10)
	rump_angle = models.DecimalField(decimal_places=2, default=0, max_digits=10)
	rump_width = models.DecimalField(decimal_places=2, default=0, max_digits=10)
	right_legs_rv = models.CharField(max_length=10, blank=True, default='')
	right_legs_sv = models.CharField(max_length=10, blank=True, default='')
	foot_angle = models.DecimalField(decimal_places=2, default=0, max_digits=10)
	locomotion = models.CharField(max_length=10, blank=True, default='')


	class Meta:
		db_table = 'cow_body_traits'


class MilkTargets(models.Model):
	cow_id = models.ForeignKey(Cow, primary_key=True, unique=True, on_delete=models.CASCADE)
	target_quantity = models.DecimalField(decimal_places=2, default=0, max_digits=10)

	class Meta:
		db_table = 'milk_targets'


class Clients(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	location = models.CharField(max_length=100, blank=True, default='')
	contacts = models.CharField(max_length=30, blank=True, default='')
	unit_price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.name

	def purchase_history_url(self):
		return ('/digitaldairy/client_purchase_history/?client_name={0}'.format(self.name))

	class Meta:
		db_table = 'clients'

class Consumers(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	location = models.CharField(max_length=100, blank=True, default='')
	contacts = models.CharField(max_length=30, blank=True, default='')
	unit_price = models.DecimalField(max_digits=10, default=0, null=True, decimal_places=2)

	def __str__(self):
		return self.name

	def consumption_history_url(self):
		return ('/digitaldairy/consumer_consumption_history/?consumer_name={0}'.format(self.name))

	class Meta:
		db_table = 'consumers'


class MilkSales(models.Model):
	id = models.AutoField(primary_key=True)
	client = models.ForeignKey(Clients, db_index=True, on_delete=models.CASCADE)
	date = models.DateField(db_column='date', db_index=True)
	quantity = models.DecimalField(max_digits=10, default=0, decimal_places=2)
	unit_price = models.DecimalField(max_digits=10, default=0, decimal_places=2)

	def __str__(self):
		return "{0} {1}".format(self.client.name, self.quantity)

	class Meta:
		unique_together = [['date', 'client']]
		index_together = [['date', 'client']]
		db_table = 'milk_sales'


class MilkConsumptions(models.Model):
	id = models.AutoField(primary_key=True)
	consumer = models.ForeignKey(Consumers, db_index=True, on_delete=models.CASCADE)
	date = models.DateField(db_column='date', db_index=True)
	quantity = models.DecimalField(max_digits=10, default=0, decimal_places=2)

	def __str__(self):
		return "{0} {1} {2}".format(self.consumer.name, self.quantity, 0)

	class Meta:
		unique_together = [['date', 'consumer']]
		index_together = [['date', 'consumer']]
		db_table = 'milk_consumption'


class MilkProductions(models.Model):
	id = models.AutoField(primary_key=True)
	milk_date = models.DateField(db_column='milk_date', db_index=True)
	cow_id = models.ForeignKey(Cow, db_column='cow_id', on_delete=models.CASCADE)
	am_quantity = models.DecimalField(decimal_places =2, null=True, default=0, max_digits=10)
	noon_quantity = models.DecimalField(decimal_places =2, null=True, default=0, max_digits=10)
	pm_quantity = models.DecimalField(decimal_places =2, null=True, default=0, max_digits=10)

	def __str__(self):
		return str(self.am_quantity + self.noon_quantity + self.pm_quantity)

	class Meta:
		unique_together = [['milk_date', 'cow_id']]
		index_together = [['milk_date', 'cow_id']]
		db_table = 'milk_production'


class WeightRecords(models.Model):
	id = models.AutoField(primary_key=True)
	weight_date = models.DateField(db_column='weight_date', db_index=True)
	cow = models.ForeignKey(Cow, db_column='cow', db_index=True, on_delete=models.CASCADE)
	weight = models.DecimalField(decimal_places =2, default=0, max_digits=10)
	height = models.DecimalField(decimal_places =2, null=True, default=0, max_digits=10)

	def __str__(self):
		return '{0} {1}'.format(self.cow.id, self.weight)

	class Meta:
		ordering = ['cow', '-weight_date']
		unique_together = [['cow', 'weight_date']]
		index_together = [['weight_date', 'cow']]
		db_table = 'weight_records'


class CowSales(models.Model):
	cow = models.ForeignKey(Cow, db_column='cow', primary_key=True, on_delete=models.CASCADE)
	client_name = models.CharField(max_length=100, blank=True, default='')
	date = models.DateField(db_column='date')
	cow_value = models.DecimalField(max_digits=10, default=0, decimal_places=2)
	sale_remarks = models.CharField(max_length=100, blank=True, default='')

	def __str__(self):
		return "{0} {1}".format(self.cow.name, self.cow_value)


	class Meta:
		db_table = 'cow_sales'


class TreatmentRecords(models.Model):
	id = models.AutoField(primary_key=True)
	cow = models.ForeignKey(Cow, db_column='cow', db_index=True, on_delete=models.CASCADE)
	diagnosis = models.CharField(max_length=100, blank=True, default='')
	disease = models.CharField(max_length=100, blank=True, default='')
	date = models.DateField(db_index=True)
	treatment_cost = models.DecimalField(max_digits=10, default=0, decimal_places=2)
	treatment = models.CharField(max_length=100, blank=True, default='')
	vet_name = models.CharField(max_length=100, blank=True, default='')

	def __str__(self):
		return "{0} {1}".format(self.disease, self.treatment)

	def get_treatment_history_url(self):
		return '/digitaldairy/cow_health/?cow_id={0}'.format(self.cow)

	class Meta:
		db_table = 'treatment_records'


class Deworming(models.Model):
	id = models.AutoField(primary_key=True)
	cow = models.ForeignKey(Cow, db_column='cow', db_index=True, on_delete=models.CASCADE)
	dewormer = models.CharField(max_length=100, blank=True, default='')
	deworming_date = models.DateField(db_index=True, db_column='date')
	next_deworming_date = models.DateField(null=True)
	deworming_cost = models.DecimalField(max_digits=10, default=0, decimal_places=2)

	def __str__(self):
		return "{0} {1}".format(self.cow, self.dewormer)

	def get_deworming_history_url(self):
		return ('/digitaldairy/deworming/?cow_id={0}'.format(self.cow))

	class Meta:
		unique_together = [['deworming_date', 'cow']]
		index_together = [['deworming_date', 'cow']]
		db_table = 'deworming_records'


class Vaccinations(models.Model):
	id = models.AutoField(primary_key=True)
	cow = models.ForeignKey(Cow, db_column='cow', db_index=True, on_delete=models.CASCADE)
	vaccine = models.CharField(max_length=100, blank=True, default='')
	vaccination_date = models.DateField(db_index=True, db_column='date')
	next_vaccination_date = models.DateField(null=True)
	vaccination_cost = models.DecimalField(max_digits=10, default=0, decimal_places=2)

	def __str__(self):
		return "{0} {1}".format(self.cow, self.vaccine)

	def get_vaccination_history_url(self):
		return ('/digitaldairy/vaccinations/?cow_id={0}'.format(self.cow))

	class Meta:
		index_together = [['vaccination_date', 'cow']]
		db_table = 'vaccinations_records'


class Diseases(models.Model):
	id = models.AutoField(primary_key=True)
	date_discovered = models.DateField()
	name = models.CharField(max_length=100)
	details = models.CharField(max_length=1000, blank=True, default='')

	class Meta:
		db_table='disease_records'


class Deaths(models.Model):
	cow = models.ForeignKey(Cow, db_column='cow', primary_key=True, on_delete=models.CASCADE)
	death_date = models.DateField(null=True)
	death_cause = models.CharField(max_length=100, blank=True, default='')
	autopsy_date = models.DateField(null=True)
	autopsy_results = models.CharField(max_length=255, blank=True, default='')
	autopsy_cost = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)
	vet_name = models.CharField(max_length=100, blank=True, default='')

	def __str__(self):
		return "{0} {1}".format(self.cow, self.death_date)

	class Meta:
		db_table = 'death_records'


class MilkSalesPayments(models.Model):
	id = models.AutoField(primary_key=True)
	client = models.ForeignKey(Clients,on_delete=models.CASCADE)
	amount_paid = models.DecimalField(max_digits=20, null=True, default=0, decimal_places=2)
	date_of_payment = models.DateField()
	milk_sale_date = models.DateField()

	@property
	def balance(self):
		milk_sales_for_date = MilkSales.objects.filter(date=self.milk_sale_date, client=self.client)
		total_milk_sale = sum([milk_sale.quantity * milk_sale.unit_price for milk_sale in milk_sales_for_date])
		return total_milk_sale - self.amount_paid

	class Meta:
		db_table = 'milk_sales_payments'


class AiRecords(models.Model):
	id = models.AutoField(primary_key=True)
	cow = models.ForeignKey(Cow, db_index=True, db_column='cow', on_delete=models.CASCADE)
	# this needs to changed so that the field is not nullable
	semen_record = models.ForeignKey(SemenRecords, on_delete=models.CASCADE)
	service_date = models.DateField(db_index=True)
	cost = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)
	vet_name = models.CharField(max_length=100, blank=True, default='')
	open_days = models.IntegerField(null=True, default=0)
	repeats = models.IntegerField(null=True, default=0)
	inbreeding = models.CharField(max_length=5, default="False",choices=[("True", "True"),("False", "False")])
	first_heat_check_date = models.DateField(null=True)
	second_heat_check_date = models.DateField(null=True)
	drying_date = models.DateField(null=True)
	steaming_date = models.DateField(null=True)
	pregnancy_check_date = models.DateField(null=True)
	pregnancy_diagnosis_date = models.DateField(null=True)
	pregnancy_diagnosis_cost = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)
	pregnancy_diagnosis_vet_name = models.CharField(max_length=100, blank=True, default='')
	pregnancy_diagnosis_result = models.CharField(max_length=20, default="Unconfirmed", choices=[('Positive', 'Positive'), ('Negative', 'Negative'), ('Unconfirmed', 'Unconfirmed'), ('Failed', 'Failed')])
	calving_status = models.CharField(max_length=100, default="Not Yet", choices=[("Not Yet", "Not Yet"), ("Calved", "Calved"),("Miscarriaged", "Miscarriaged"), ("Aborted","Aborted")])
	due_date = models.DateField(null=True)

	def __str__(self):
		return "{0} {1}".format(self.cow.name, self.service_date)

	class Meta:
		ordering = ['-service_date']
		index_together = [['service_date', 'cow']]
		unique_together = [['service_date', 'cow']]
		db_table = 'ai_records'


class Calvings(models.Model):
	ai_record = models.ForeignKey(AiRecords, db_column='ai_record', primary_key=True, on_delete=models.CASCADE)
	calf = models.ForeignKey(Cow, db_index=True, db_column='calf', on_delete=models.CASCADE)
	calving_date = models.DateField()
	calving_type = models.CharField(max_length=7, default='Single', choices=[('Single', 'Single'), ('Twin', 'Twin')])

	def __str__(self):
		return "{0} {1} {2}".format(self.ai_record.cow, self.calf, self.calving_date)

	def progeny(self):
		if self.ai_record:
			if self.ai_record.cow:
				return Cow.objects.filter(dam=self.ai_record.cow, dob__lt=self.ai_record.cow.dob).count()
			return 1
		return 1

	def calving_interval(self):
		calving_list_after_this = Calvings.objects.filter(ai_record__cow = self.ai_record.cow, calving_date__gt=self.calving_date)
		if len(calving_list_after_this) > 0:
			return (calving_list_after_this[0].calving_date - self.calving_date).days
		else:
			return (datetime.date.today() - self.calving_date).days

	class Meta:
		db_table = 'calving_records'


class AbortionMiscarriages(models.Model):
	ai_record = models.ForeignKey(AiRecords,  db_column='ai_record', on_delete=models.CASCADE, primary_key=True)
	date = models.DateField()
	type = models.CharField(max_length=20, choices=[('Miscarriage', 'Miscarriage'),
	                                                ('Abortion', 'Abortion')])
	cost = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)
	cause = models.CharField(max_length=1000, blank=True, default='')
	vet_name = models.CharField(max_length=100, blank=True, default='')

	def __str__(self):
		return "{0} {1}".format(self.ai_record.cow.id, self.type)

	class Meta:
		db_table = 'abortion_miscarriages'


class Employees(models.Model):
	id = models.CharField(max_length=30, primary_key=True)
	date_hired = models.DateField(null=True)
	salary = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)
	name = models.CharField(max_length=100)
	department = models.CharField(max_length=100, blank=True, default='')
	designation = models.CharField(max_length=100, blank=True, default='')
	contacts = models.CharField(max_length=100, blank=True, default='')


	def __str__(self):
		return "{0}".format(self.name)

	class Meta:
		db_table = 'employees'


class salaries_and_advances(models.Model):
	id = models.AutoField(primary_key=True)
	employee = models.ForeignKey(Employees, db_index=True, db_column='employee', on_delete=models.CASCADE)
	advance_date = models.DateField(null=True)
	salary_date = models.DateField(null=True)
	ending_month_date = models.DateField(null=True)
	advance_amount = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)
	salary_amount = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)
	balance_after_salary = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)
	balance_after_advance = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)


	def __str__(self):
		return "{0} {1}".format(self.employee.name, self.salary_amount)

	class Meta:
		db_table = 'salaries_advances'


class CalfFeeding(models.Model):
	id = models.AutoField(primary_key=True)
	cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
	milk_quantity = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)
	feeding_date = models.DateField()

	class Meta:
		db_table = 'calf_feeding'


class FeedItems(models.Model):
	name = models.CharField(max_length=100, primary_key=True)
	unit_of_measure = models.CharField(max_length=30, blank=True, default='')
	unit_price = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)
	initial_stock = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)
	available_stock = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)
	reorder_level = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)


	def __str__(self):
		return "{0}".format(self.name)

	class Meta:
		db_table = 'feed_item'


class FeedFormulation(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30, unique=True, default='')
	quantity = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)

	class Meta:
		db_table = 'feed_formulation'


class FeedFormulationPart(models.Model):
	id = models.AutoField(primary_key=True)
	feed_item = models.ForeignKey(FeedItems, on_delete=models.CASCADE)
	feed_formulation = models.ForeignKey(FeedFormulation, on_delete=models.CASCADE)
	quantity = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)


	class Meta:
		index_together = [['feed_item', 'feed_formulation']]
		unique_together = [['feed_item', 'feed_formulation']]
		db_table = 'feed_formulation_part'


class FeedingProgramme(models.Model):
	id = models.AutoField(primary_key=True)
	quantity = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)
	feed_formulation = models.ForeignKey(FeedFormulation, on_delete=models.CASCADE)
	feeding_category = models.CharField(max_length=30, default="Heifer",
	                                    choices=[('Milker', 'Milker'), ('Heifer', 'Heifer'), ('Dry', 'Dry'),
	                                             ('Steamer', 'Steamer'), ('Incalf Heifer', 'Incalf Heifer'),
	                                             ('Calf', 'Calf'), ('Weaner', 'Weaner'), ('Weaner 1', 'Weaner 1'),('Weaner 2', 'Weaner 2'), ('Weaner 3', 'Weaner 3'), ('Yearling', 'Yearling'), ('Bulling', 'Bulling'), ('Bull', 'Bull')])

	class Meta:
		db_table = 'feeding_programme'


class DailyFeeding(models.Model):
	id = models.AutoField(primary_key=True)
	date = models.DateField()
	quantity = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)
	feed_formulation = models.ForeignKey(FeedFormulation, on_delete=models.CASCADE)
	feeding_category = models.CharField(max_length=30, default="Heifer",
	                                    choices=[('Milker', 'Milker'), ('Heifer', 'Heifer'), ('Dry', 'Dry'),
	                                             ('Steamer', 'Steamer'), ('Incalf Heifer', 'Incalf Heifer'),
	                                             ('Calf', 'Calf'), ('Weaner', 'Weaner'), ('Weaner 1', 'Weaner 1'),
	                                             ('Weaner 2', 'Weaner 2'), ('Weaner 3', 'Weaner 3'),
	                                             ('Yearling', 'Yearling'), ('Bulling', 'Bulling'), ('Bull', 'Bull')])

	class Meta:
		db_table = 'daily_feeding'


class CowInsurance(models.Model):
	id = models.AutoField(primary_key=True)
	cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
	policy = models.CharField(max_length=30, blank=True, default='')
	from_date = models.DateField()
	to_date = models.DateField()
	insured_value = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)
	premium_amount = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)


	class Meta:
		db_table = 'cow_insurance'


class Expense(models.Model):
	id = models.AutoField(primary_key=True)
	date = models.DateField()
	amount = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)
	source = models.CharField(max_length=30, blank=True, default='')


	class Meta:
		db_table = 'expense'


class Income(models.Model):
	id = models.AutoField(primary_key=True)
	date = models.DateField()
	amount = models.DecimalField(max_digits=10, null=True, default=0, decimal_places=2)
	source = models.CharField(max_length=30, blank=True, default='')


	class Meta:
		db_table = 'income'

