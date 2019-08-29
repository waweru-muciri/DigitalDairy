from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import  login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from .models import *
import datetime
import dateutil.relativedelta
import itertools
import collections
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.


general_to_date = datetime.date.today()
general_from_date = datetime.date(2000,1,1)


@require_http_methods(['GET'])
def index(request):
	context = {
	}
	return render(request, context=context, template_name='digitaldairy/html/landing-page.html')


@require_http_methods(['POST'])
def send_message(request):
	senders_email = request.POST['email']
	senders_phone_number = request.POST['phone_number']
	senders_first_name = request.POST['first_name'].strip().title()
	senders_last_name = request.POST['last_name'].strip().title()
	message = request.POST.get('message')
	if len(senders_first_name) < 4:
		messages.error(request, "Your first name must be a minimum of four letters")
		return render(request, template_name='digitaldairy/html/landing-page.html')
	if len(senders_last_name) < 4:
		messages.error(request, "Your last name must be a minimum of four letters")
		return render(request, template_name='digitaldairy/html/landing-page.html')

	if len(senders_phone_number) < 10 and not senders_phone_number.isdigit():
		messages.error(request, "Your phone number is invalid")
		return render(request, template_name='digitaldairy/html/landing-page.html')

	if len(message) < 4:
		messages.error(request, "Your last name must be a minimum of four letters")
		return render(request, template_name='digitaldairy/html/landing-page.html')

	messages.success(request, "Message sent successfully!")
	messages.success(request, "We will get back to you shortly!")
	send_mail('Hi, ' + senders_email + ' wants your software!', message, 'smartfarmsoftwares@gmail.com', recipient_list=['bwwaweru18@gmail.com'], fail_silently=False)
	# return a different view showing the user that the message has been sent
	return HttpResponseRedirect(reverse('digitaldairy:home'))



@login_required
@require_http_methods(['GET'])
def cows(request):
	cows_list = Cow.objects.all()
	context = {
		'cows_list': cows_list,
	}
	return render(request, context=context, template_name='digitaldairy/html/cows.html')


@login_required
@require_http_methods(['GET'])
def daily_milk_production(request):
	milk_production_date = request.GET.get('milk_production_date')
	milk_production_date = milk_production_date if milk_production_date else request.session.get('milk_production_date')
	if milk_production_date is None:
		milk_production_date = general_to_date
	else:
		try:
			milk_production_date = datetime.datetime.strptime(milk_production_date, '%Y-%m-%d').date()
		except:
			milk_production_date = general_to_date
	day_milk_production = MilkProductions.objects.filter(milk_date=milk_production_date)
	previous_date = milk_production_date - dateutil.relativedelta.relativedelta(days=1)
	previous_day_milk_production = MilkProductions.objects.filter(milk_date=previous_date)
	totals_list = []
	for milk_p in day_milk_production:
		cow_previous_day_milk_p = previous_day_milk_production.filter(cow_id=milk_p.cow_id)
		cow_day_milk_production_total = sum((milk_p.am_quantity,milk_p.noon_quantity, milk_p.pm_quantity))
		if cow_previous_day_milk_p.count() > 0:
			cow_previous_day_milk_p = cow_previous_day_milk_p[0]
			total_previous_day_milk_p =  sum((cow_previous_day_milk_p.am_quantity,cow_previous_day_milk_p.noon_quantity, cow_previous_day_milk_p.pm_quantity))
		else:
			total_previous_day_milk_p = 0
		difference = cow_day_milk_production_total - total_previous_day_milk_p
		totals_list.append({'cow':milk_p.cow_id, 'difference': difference})
	day_and_previous_day_totals_sorted = sorted(totals_list, key=lambda x:x['difference'], reverse=True)
	# get all cows to pass on to the template
	all_cows = Cow.objects.all().values()
	# get all milk targets
	milk_production_targets_list = MilkTargets.objects.all()
	total_day_milk_production = sum([(cow_milk_production.am_quantity + cow_milk_production.noon_quantity + cow_milk_production.pm_quantity) for cow_milk_production in day_milk_production])
	average_milk_quantity = total_day_milk_production / day_milk_production.count() if len(day_milk_production) > 0 else 0
	un_milked_cows = len(all_cows) - day_milk_production.count()
	day_milk_production = sorted(day_milk_production,key= lambda x: (x.am_quantity + x.noon_quantity + x.pm_quantity),reverse=True)

	context = {
		'day_and_previous_day_totals_sorted': day_and_previous_day_totals_sorted,
		'unmilked_cows': un_milked_cows,
		'average_milk_quantity' : average_milk_quantity,
		'total_day_milk_production': total_day_milk_production,
		'milk_production_targets_list': milk_production_targets_list,
		'all_cows': all_cows,
		'milk_date': milk_production_date,
		'milk_production_list': day_milk_production,
	}
	return render(request, context=context, template_name='digitaldairy/html/milk-production.html')


@login_required
@require_http_methods(['GET'])
def monthly_milk_production(request):
	month = request.GET.get('month')
	year = request.GET.get('year')
	if year:
		try:
			year = int(year)
			year = 1 if year < 1 else year
		except ValueError:
			year = datetime.date.today().year
	else:
		year = datetime.date.today().year
	if month:
		try:
			month = int(month)
			month = 1 if (month > 12 or month < 1) else month
		except ValueError:
			month = 1
	else:
		month = datetime.date.today().month
	selected_month_date = datetime.date(year=year, month=month, day=1)
	previous_month_date = selected_month_date - dateutil.relativedelta.relativedelta(months=1)
	selected_month_milk_production_list = MilkProductions.objects.all().filter(milk_date__month=month, milk_date__year=year)
	previous_month_milk_production_list = MilkProductions.objects.all().filter(milk_date__month=previous_month_date.month, milk_date__year=previous_month_date.year)
	# calculate total selected month milk quantity
	total_selected_month_milk_quantity = sum([selected_month_milk_production.get('am_quantity')+ selected_month_milk_production.get('noon_quantity') + selected_month_milk_production.get('pm_quantity') for selected_month_milk_production in selected_month_milk_production_list.values()])
	# group month milk production by cow by sorting first
	selected_month_milk_production_list = sorted(selected_month_milk_production_list, key=lambda x:x.cow_id.id)
	previous_month_milk_production_list = sorted(previous_month_milk_production_list, key=lambda x:x.cow_id.id)
	milk_production_list = []
	previous_month_milk_production_dict = {}
	for key, group in itertools.groupby(previous_month_milk_production_list, lambda x: x.cow_id.id):
		previous_month_milk_production_dict[key] = list(group)
	cows_that_produced_milk_in_selected_month = []
	for key, group in itertools.groupby(selected_month_milk_production_list,lambda x:x.cow_id.id):
		cows_that_produced_milk_in_selected_month.append(key)
		selected_month_cow_milk_production_list =  list(group)
		total_selected_month_quantity = sum([milk_p.am_quantity + milk_p.noon_quantity + milk_p.pm_quantity for milk_p in selected_month_cow_milk_production_list])
		previous_month_cow_milk_production_list = previous_month_milk_production_dict.get(key, [])
		total_previous_month_quantity = sum([milk_p.am_quantity + milk_p.noon_quantity + milk_p.pm_quantity for milk_p in previous_month_cow_milk_production_list])
		months_milk_difference = total_selected_month_quantity - total_previous_month_quantity
		daily_average = total_selected_month_quantity / len(selected_month_cow_milk_production_list) \
			if len(selected_month_cow_milk_production_list) > 0 else 0
		milk_production_list.append({'cow_id': selected_month_cow_milk_production_list[0].cow_id,
		                             'total_selected_month_quantity': total_selected_month_quantity ,
		                             'total_previous_month_quantity': total_previous_month_quantity,
		                             'months_milk_difference': months_milk_difference,
		                             'daily_average' : daily_average,
		                             })
	for milk_p in milk_production_list:
		cow_milk_target = MilkTargets.objects.filter(cow_id=milk_p['cow_id'])
		milk_p['monthly_milk_target'] = cow_milk_target[0].target_quantity * 30 if cow_milk_target.count() > 0 else 0
		milk_p['variance'] = milk_p['monthly_milk_target'] - milk_p['total_selected_month_quantity']
	milk_production_list = sorted(milk_production_list, key = lambda x:x.get('total_selected_month_quantity',0), reverse=True)
	context = {
		'average_cow_milk_quantity': total_selected_month_milk_quantity / len(milk_production_list) if len(milk_production_list) > 0 else 0,
		'total_selected_month_milk_quantity': total_selected_month_milk_quantity,
		'selected_month_date': selected_month_date,
		'previous_month_date': previous_month_date,
		'milk_production_list': milk_production_list,
	}
	return render(request, context=context, template_name='digitaldairy/html/monthly-milk-production.html')


@login_required
@require_http_methods(['GET'])
def get_sales_statistics(request):
	month = request.GET.get('month')
	year = request.GET.get('year')
	if month:
		try:
			month = int(month)
		except:
			month = datetime.date.today().month
	else:
		month = datetime.date.today().month
	if year:
		try:
			year = int(year)
		except:
			year = datetime.date.today().year
	else:
		year = datetime.date.today().year
	current_received_date = datetime.date(year, month, 1)
	year_milk_sales = MilkSales.objects.filter(date__year=year)
	month_milk_sales = year_milk_sales.filter(date__month=month)
	year_milk_sales = sorted(year_milk_sales, key=lambda x: x.date.month)
	# this is pretty sweet
	grouped_yearly_milk_sales_dict = {}
	for month, month_milk_sale_list in itertools.groupby(year_milk_sales, key=lambda x: x.date.month):
		grouped_yearly_milk_sales_dict[month] = sum([milk_sale.quantity * milk_sale.client.unit_price for milk_sale in list(month_milk_sale_list)])
	grouped_yearly_milk_sale = sorted(list(grouped_yearly_milk_sales_dict.items()), key=lambda x: x[1], reverse=True)
	starting_month = 0
	while starting_month < 12:
		grouped_yearly_milk_sales_dict[starting_month] = grouped_yearly_milk_sales_dict.get(starting_month, 0)
		starting_month += 1
	highest_month_milk_sale = grouped_yearly_milk_sale[0][1] if len(grouped_yearly_milk_sale) > 0 else 0
	lowest_month_milk_sale = grouped_yearly_milk_sale[-1][1] if len(grouped_yearly_milk_sale) > 0 else 0
	total_year_milk_sales = sum([milk_sale.quantity * milk_sale.client.unit_price for milk_sale in year_milk_sales])
	total_year_milk_sales_quantity = sum([milk_sale.quantity for milk_sale in year_milk_sales])
	month_milk_sales = sorted(month_milk_sales, key=lambda x: x.date)
	# calculate total daily milk production
	total_daily_milk_sale_dict = {}
	for day, day_milk_sale_list in itertools.groupby(month_milk_sales, key=lambda x: x.date):
		total_daily_milk_sale_dict[day] = sum([milk_sale.quantity * milk_sale.client.unit_price for milk_sale in list(day_milk_sale_list)])
	# grab the lowest and highest milk production quantities
	lowest_day_sale = sorted(total_daily_milk_sale_dict.items(), key=lambda x: x[0])[-1][1] if len(total_daily_milk_sale_dict) > 0 else 0
	highest_day_sale = sorted(total_daily_milk_sale_dict.items(), reverse=True, key=lambda x: x[1])[0][1] if len(total_daily_milk_sale_dict) > 0 else 0
	end_month_date = current_received_date + dateutil.relativedelta.relativedelta(months=1)
	month_starting_date = current_received_date
	while month_starting_date < end_month_date:
		total_daily_milk_sale_dict[month_starting_date] = total_daily_milk_sale_dict.get(month_starting_date, 0)
		month_starting_date = month_starting_date + datetime.timedelta(days=1)
	total_daily_milk_sale_dict = collections.OrderedDict(
		sorted(total_daily_milk_sale_dict.items(), key=lambda x: x[0]))
	total_month_milk_sales = sum([milk_sale.quantity * milk_sale.client.unit_price for milk_sale in month_milk_sales])
	total_month_milk_sales_quantity = sum([milk_sale.quantity for milk_sale in month_milk_sales])
	average_daily_milk_sale_quantity = total_month_milk_sales_quantity / len(total_daily_milk_sale_dict) if len(total_daily_milk_sale_dict) > 0 else 0
	average_daily_milk_sale = total_month_milk_sales / len(total_daily_milk_sale_dict) if len(total_daily_milk_sale_dict) > 0 else 0
	context = {
		'grouped_yearly_milk_sales_dict': grouped_yearly_milk_sales_dict.items(),
		'total_daily_milk_sale_dict': total_daily_milk_sale_dict.items(),
		'highest_month_milk_sale': highest_month_milk_sale,
		'lowest_month_milk_sale': lowest_month_milk_sale,
		'current_date': current_received_date,
		'total_year_milk_sales': total_year_milk_sales,
		'total_year_milk_sales_quantity': total_year_milk_sales_quantity,
		'highest_day_sale': highest_day_sale,
		'lowest_day_sale': lowest_day_sale,
		'average_daily_milk_sale_quantity': average_daily_milk_sale_quantity,
		'average_daily_milk_sale': average_daily_milk_sale,
		'average_monthly_milk_sales': total_year_milk_sales / 12,
		'total_month_milk_sales_quantity': total_month_milk_sales_quantity,
		'total_month_milk_sales': total_month_milk_sales,
	}
	return render(request, context=context, template_name='digitaldairy/html/milk-sales-statistics.html')


@login_required
@require_http_methods(['GET', 'POST'])
def cow_feeds(request):
	if request.method == 'POST':
		feeding_programme_id = request.POST.get('feeding_programme_id')
		feed_formulation_id = request.POST.get('feed_formulation_id')
		feed_formulation = get_object_or_404(FeedFormulation, pk=feed_formulation_id)
		feed_quantity = request.POST.get('feed_quantity')
		feeding_category = request.POST.get('feeding_category')
		feeding_programme = FeedingProgramme()
		feeding_programme.id = feeding_programme_id
		feeding_programme.feeding_category = feeding_category
		feeding_programme.feed_formulation = feed_formulation
		feeding_programme.quantity = feed_quantity
		feeding_programme.save()
	feeds_list = FeedItems.objects.all()
	feed_formulations_list = FeedFormulation.objects.all()
	feeding_programmes_list = FeedingProgramme.objects.all()
	context = {
		'feeds_list': feeds_list,
		'feeding_programmes_list': feeding_programmes_list,
		'feed_formulations_list': feed_formulations_list,
	}
	return render(request, context=context, template_name='digitaldairy/html/cow-feeds.html')


@login_required
@require_http_methods(['GET'])
def cow_feed_items(request):

	feeds_list = FeedItems.objects.all()
	context = {
		'feeds_list': feeds_list,
	}
	return render(request, context=context, template_name='digitaldairy/html/feed-items.html')


@login_required
@require_http_methods(['GET'])
def daily_feeding(request):
	feed_formulations_list = FeedFormulation.objects.all()
	daily_feeding_list = DailyFeeding.objects.all()
	context = {
		'daily_feeding_list': daily_feeding_list,
		'feed_formulations_list': feed_formulations_list,
	}
	return render(request, context=context, template_name='digitaldairy/html/daily-feeding.html')


@login_required
@require_http_methods(['GET'])
def get_cow_sales(request):
	cow_sales_list = CowSales.objects.all()
	gross_cow_sales = sum(cow_sale.cow_value for cow_sale in cow_sales_list)
	cows_list = Cow.objects.all()
	context = {
		'gross_cow_sales': gross_cow_sales,
		'cows_list': cows_list,
		'cow_sales_list': cow_sales_list
	}
	return render(request, context=context, template_name='digitaldairy/html/cow-sales.html')


@login_required
@require_http_methods(['GET', 'POST'])
def calf_management(request):
	if request.method == 'POST':
		calf_feeding_id = request.POST.get('calf_feeding_id')
		feeding_date = request.POST.get('feeding_date')
		calf_id = request.POST.get('calf_id')
		referenced_calf = get_object_or_404(Cow, pk=calf_id)
		milk_quantity = request.POST.get('milk_quantity')
		calf_feeding = CalfFeeding()
		calf_feeding.id = calf_feeding_id
		calf_feeding.feeding_date = feeding_date
		calf_feeding.cow = referenced_calf
		calf_feeding.milk_quantity = milk_quantity
		calf_feeding.save()
	weight_objects_list = WeightRecords.objects.all()
	weight_list = []
	for _, group in itertools.groupby(weight_objects_list, lambda x: x.cow.id):
		individual_cow_weight_list = tuple(group)
		individual_cow_weight_list_length = len(individual_cow_weight_list)
		for i in range(individual_cow_weight_list_length):
			weight_change = (individual_cow_weight_list[i].weight - individual_cow_weight_list[
								i + 1].weight) if i + 1 < individual_cow_weight_list_length else 0
			if weight_change > 0:
				weight_change = 'Gain ({0})'.format(weight_change)
			elif weight_change == 0:
				weight_change = 'Maintained ({0})'.format(weight_change)
			else:
				weight_change = 'Loss ({0})'.format(weight_change)
			weight_list.append({
				'cow': individual_cow_weight_list[i].cow,
				'id': individual_cow_weight_list[i].id,
				'weight': individual_cow_weight_list[i].weight,
				'height': individual_cow_weight_list[i].height,
				'weight_date': individual_cow_weight_list[i].weight_date,
				'status': weight_change
			})
	all_calves = Cow.objects.all()
	calf_feeding_list = CalfFeeding.objects.all()
	context = {
		'weight_list' : weight_list,
		'all_calves': all_calves,
		'calf_feeding_list': calf_feeding_list,
	}
	return render(request, context=context, template_name='digitaldairy/html/calf-management.html')


@login_required
@require_http_methods(['GET'])
def get_weight_recording(request):
	weight_objects_list = WeightRecords.objects.all()
	weight_list = []
	for _, group in itertools.groupby(weight_objects_list, lambda x: x.cow.id):
		individual_cow_weight_list = tuple(group)
		individual_cow_weight_list_length = len(individual_cow_weight_list)
		for index in range(individual_cow_weight_list_length):
			weight_change =  (individual_cow_weight_list[index].weight - individual_cow_weight_list[index+1].weight) if index+1 < individual_cow_weight_list_length else 0
			weight_change = 'Gain ({0})'.format(weight_change) if weight_change >= 0 else 'Loss ({0})'.format(weight_change)
			weight_list.append({
			'cow' : individual_cow_weight_list[index].cow,
			'id': individual_cow_weight_list[index].id,
			'weight': individual_cow_weight_list[index].weight,
			'height': individual_cow_weight_list[index].height,
			'weight_date': individual_cow_weight_list[index].weight_date,
			'status': weight_change
			})

	cows_list = Cow.objects.all()
	context = {
		'cows_list': cows_list,
		'weight_list': weight_list
	}
	return render(request, context=context, template_name='digitaldairy/html/weight-recording.html')


@login_required
@require_http_methods(['POST'])
def save_weight(request):
	weight_record_id = request.POST.get('weight_id')
	cow_id = request.POST.get('cow_id')
	referenced_cow = get_object_or_404(Cow, pk=cow_id)
	weight_date = request.POST.get('weight_date')
	weight = request.POST.get('animal_weight')
	height = request.POST.get('animal_height')
	weight_record = WeightRecords(id=weight_record_id, cow=referenced_cow, weight_date=weight_date, weight=weight, height=height)
	weight_record.save()
	return HttpResponseRedirect('/digitaldairy/weight_recording/')


@login_required
@require_http_methods(['GET'])
def get_cow_health(request):
	cow_id = request.GET.get('cow_id')
	if cow_id:
		referenced_cow = get_object_or_404(Cow, pk=cow_id)
		treatment_records_list = TreatmentRecords.objects.filter(cow=referenced_cow)
	else:
		treatment_records_list = TreatmentRecords.objects.all()
	all_cows = Cow.objects.all()
	context = {
		'all_cows': all_cows,
		'treatment_records_list' : treatment_records_list
	}
	return render(request, context=context, template_name='digitaldairy/html/cow-health.html')


@login_required
@require_http_methods(['GET'])
def get_deworming(request):
	cow_id = request.GET.get('cow_id')
	if cow_id:
		referenced_cow = get_object_or_404(Cow, pk=cow_id)
		deworming_records_list = Deworming.objects.filter(cow=referenced_cow)
	else:
		deworming_records_list = Deworming.objects.all()
	all_cows = Cow.objects.all()
	context = {
		'all_cows': all_cows,
		'deworming_records_list': deworming_records_list
	}
	return render(request, context=context, template_name='digitaldairy/html/deworming.html')


@login_required
@require_http_methods(['GET'])
def get_vaccinations(request):
	cow_id = request.GET.get('cow_id')
	if cow_id:
		referenced_cow = get_object_or_404(Cow, pk=cow_id)
		vaccination_records_list = Vaccinations.objects.filter(cow=referenced_cow)
	else:
		vaccination_records_list = Vaccinations.objects.all()
	all_cows = Cow.objects.all()
	context = {
		'vaccination_records_list': vaccination_records_list,
		'all_cows': all_cows
	}
	return render(request, context=context, template_name='digitaldairy/html/vaccinations.html')


@login_required
@require_http_methods(['GET'])
def get_deaths_autopsy(request):
	death_records_list = Deaths.objects.all()
	death_without_autopsies_list = Deaths.objects.filter(autopsy_date=None)
	all_cows = Cow.objects.all()
	context = {
		'death_records_list' : death_records_list,
		'death_without_autopsies_list' : death_without_autopsies_list,
		'all_cows' : all_cows,

	}
	return render(request, context=context, template_name='digitaldairy/html/deaths-autopsies.html')


@login_required
@require_http_methods(['GET'])
def cow_diseases(request):
	diseases_list = Diseases.objects.all()
	context = {
		'diseases_list': diseases_list,
	}
	return render(request, context=context, template_name='digitaldairy/html/diseases.html')


@login_required
@require_http_methods(['GET'])
def get_semen_catalog(request):
	semen_catalog_list = SemenRecords.objects.all()
	context = {
		'semen_catalog_list': semen_catalog_list
	}
	return render(request, context=context, template_name='digitaldairy/html/semen-catalog.html')


@login_required
@require_http_methods(['GET'])
def get_ai_records(request):
	ai_records_list = AiRecords.objects.all()
	sorted_ai_records_list = sorted(ai_records_list, key=lambda x: (x.due_date - x.service_date).days // 30)
	pregnancy_levels_list = [(9- key, list(ai_records_iter)) for key, ai_records_iter in itertools.groupby(sorted_ai_records_list, key=lambda x: (x.due_date - general_to_date).days // 30)]
	all_cows = Cow.objects.all()
	context = {
		'pregnancy_levels_list' : pregnancy_levels_list,
		'ai_records_list': ai_records_list,
		'all_cows': all_cows,

	}
	return render(request, context=context, template_name='digitaldairy/html/ai-records.html')


@login_required
@require_http_methods(['GET'])
def get_pregnancy_diagnosis(request):
	ai_records_list = AiRecords.objects.all()
	context = {
		'ai_records_list': ai_records_list,
	}
	return render(request, context=context, template_name='digitaldairy/html/pregnancy-diagnosis.html')


@login_required
@require_http_methods(['GET'])
def calving_maternity(request):
	ai_records_list = AiRecords.objects.filter(calving_status = 'Not Yet')
	calving_records_list = Calvings.objects.all()
	context = {
		'ai_records_list': ai_records_list,
		'calving_records_list': calving_records_list,
	}
	return render(request, context=context, template_name='digitaldairy/html/calving.html')


@login_required
@require_http_methods(['GET'])
def abortions_miscarriages(request):
	ai_records_list = AiRecords.objects.all()
	abortions_miscarriages_list = AbortionMiscarriages.objects.all()
	context = {
		'abortions_miscarriages_list': abortions_miscarriages_list,
		'ai_records_list': ai_records_list,
	}
	return render(request, context=context, template_name='digitaldairy/html/abortions.html')


@login_required
@require_http_methods(['GET'])
def breeding_statistics(request):
	month = request.GET.get('month')
	year = request.GET.get('year')
	if month:
		try:
			month = int(month)
		except:
			month = general_to_date.month
	else:
		month = general_to_date.month
	if year:
		try:
			year = int(year)
		except:
			year = general_to_date.year
	else:
		year = general_to_date.year
	selected_month_date = datetime.date(year, month, 1)
	cows = Cow.objects.all()
	cows_list = []
	for cow in cows:
		cow_ai_records = AiRecords.objects.filter(cow= cow)
		total_cost = sum([ai_record.cost for ai_record in cow_ai_records])
		positive_pds = cow_ai_records.filter(pregnancy_diagnosis_result="Positive").count()
		negative_pds = cow_ai_records.filter(pregnancy_diagnosis_result="Negative").count()
		deliveries = cow_ai_records.filter(calving_status="Calved").count()
		abortions = cow_ai_records.filter(calving_status="Aborted").count()
		cow_breeding_object = {'id': cow.id, 'name': cow.name, 'category': cow.category, 'status': cow.status}
		cow_breeding_object['services'] = cow_ai_records.count()
		cow_breeding_object['positive_pregnancies'] = positive_pds
		cow_breeding_object['negative_pregnancies'] =  negative_pds
		cow_breeding_object['deliveries'] = deliveries
		cow_breeding_object['abortions'] = abortions
		cow_breeding_object['total_cost'] = total_cost
		all_descendants_of_cow = Cow.objects.filter(dam=cow)
		cow_breeding_object['males_delivered'] = all_descendants_of_cow.filter(category="Bull").count()
		cow_breeding_object['females_delivered'] = all_descendants_of_cow.count() - cow_breeding_object['males_delivered']
		cow_breeding_object['fertility_rate'] = (positive_pds / cow_ai_records.count()) * 100 if cow_ai_records.count() > 0 else 0
		cows_list.append(cow_breeding_object)
	total_ai_records = AiRecords.objects.all()
	total_services = total_ai_records.count()
	total_conceptions = total_ai_records.filter(pregnancy_diagnosis_result="Positive").count()
	total_failed = total_ai_records.filter(pregnancy_diagnosis_result="Failed").count()
	total_deliveries = total_ai_records.filter(pregnancy_diagnosis_result="Calved").count()
	conception_rate = (total_conceptions / total_services) * 100 if total_services > 0 else 0
	context = {
		'selected_month_date': selected_month_date,
		'cows_list': cows_list,
		'total_services': total_services,
		'total_conceptions': total_conceptions,
		'total_failed': total_failed,
		'total_deliveries': total_deliveries,
		'conception_rate': conception_rate,
	}
	return render(request, context=context, template_name='digitaldairy/html/breeding-statistics.html')


@login_required
@require_http_methods(['GET'])
def breeding_alerts(request):
	calvings_for_current_month = AiRecords.objects.filter(due_date__month=general_to_date.month)
	steamings_for_current_month = AiRecords.objects.filter(steaming_date__month=general_to_date.month)
	dryings_for_current_month = AiRecords.objects.filter(drying_date__month=general_to_date.month)
	context = {
		'current_date': general_to_date,
		"calvings_for_current_month": calvings_for_current_month,
		"steamings_for_current_month": steamings_for_current_month,
		"dryings_for_current_month": dryings_for_current_month,

	}
	return render(request, context=context, template_name='digitaldairy/html/breeding-alerts.html')


@login_required
@require_http_methods(['GET'])
def get_milk_production_statistics(request):
	month = request.GET.get('month')
	year = request.GET.get('year')
	if month:
		try:
			month = int(month)
		except:
			month = general_to_date.month
	else:
		month = general_to_date.month
	if year:
		try:
			year = int(year)
		except:
			year = general_to_date.year
	else:
		year = general_to_date.year
	current_received_date = datetime.date(year, month, 1)
	year_milk_production = MilkProductions.objects.filter(milk_date__year=year)
	month_milk_production = year_milk_production.filter(milk_date__month=month)
	year_milk_production = sorted(year_milk_production, key=lambda x: x.milk_date.month)
	# this is pretty sweet
	grouped_yearly_milk_production_dict = {}
	for month, month_milk_p_list in itertools.groupby(year_milk_production, key=lambda x:x.milk_date.month):
		grouped_yearly_milk_production_dict[month] = sum([sum([milk_p.am_quantity, milk_p.noon_quantity, milk_p.pm_quantity]) for milk_p in list(month_milk_p_list)])
	grouped_yearly_milk_production = sorted(list(grouped_yearly_milk_production_dict.items()), key=lambda x:x[1],reverse=True)
	starting_month = 1
	while starting_month < 13:
		grouped_yearly_milk_production_dict[starting_month] = grouped_yearly_milk_production_dict.get(starting_month, 0)
		starting_month +=1
	highest_month_milk_quantity = grouped_yearly_milk_production[0][1] if len(grouped_yearly_milk_production) > 0 else 0
	lowest_month_milk_quantity = grouped_yearly_milk_production[-1][1] if len(grouped_yearly_milk_production) > 0 else 0
	total_year_milk_production = sum(
		[sum((milk_p.am_quantity, milk_p.noon_quantity, milk_p.pm_quantity)) for milk_p in year_milk_production])
	month_milk_production = sorted(month_milk_production, key=lambda x: x.milk_date)
	# calculate total daily milk production
	total_daily_milk_production_dict = {}
	for day, day_milk_p_list in itertools.groupby(month_milk_production, key= lambda x:x.milk_date):
		total_daily_milk_production_dict[day] = sum([sum([milk_p.am_quantity, milk_p.noon_quantity,
		                                                  milk_p.pm_quantity]) for milk_p in list(day_milk_p_list)])
	# grab the lowest and highest milk production quantities
	lowest_day_quantity =  sorted(total_daily_milk_production_dict.items(), key=lambda x:x[0])[-1][1] if len(total_daily_milk_production_dict) > 0 else 0
	highest_day_quantity = sorted(total_daily_milk_production_dict.items(), reverse=True, key=lambda x:x[1])[0][1] if len(total_daily_milk_production_dict) > 0 else 0
	end_month_date = current_received_date + dateutil.relativedelta.relativedelta(months=1)
	month_starting_date = current_received_date
	while month_starting_date < end_month_date:
		total_daily_milk_production_dict[month_starting_date] = total_daily_milk_production_dict.get(month_starting_date, 0)
		month_starting_date = month_starting_date + datetime.timedelta(days=1)
	total_daily_milk_production_dict = collections.OrderedDict(
		sorted(total_daily_milk_production_dict.items(), key=lambda x: x[0]))
	total_month_milk_production = sum(
		[sum((milk_p.am_quantity, milk_p.noon_quantity, milk_p.pm_quantity)) for milk_p in month_milk_production])
	average_daily_milk_quantity = total_month_milk_production / len(total_daily_milk_production_dict)  if len(total_daily_milk_production_dict) > 0 else 0
	context = {
		'grouped_yearly_milk_production_dict': grouped_yearly_milk_production_dict.items(),
		'total_daily_milk_production_dict': total_daily_milk_production_dict.items(),
		'highest_month_milk_quantity': highest_month_milk_quantity,
		'lowest_month_milk_quantity': lowest_month_milk_quantity,
		'current_date': current_received_date,
		'total_year_milk_production': total_year_milk_production,
		'highest_day_quantity': highest_day_quantity,
		'lowest_day_quantity': lowest_day_quantity,
		'average_daily_milk_quantity' : average_daily_milk_quantity,
		'average_monthly_milk_quantity' : total_year_milk_production / 12,
		'total_month_milk_production': total_month_milk_production,
	}
	return render(request, context=context, template_name='digitaldairy/html/milk-production-statistics.html')


@login_required
@require_http_methods(['GET', 'POST'])
def cow_profile(request):
	if request.method == 'POST':
		cow_id = request.POST.get('cow_id')
		referenced_cow = get_object_or_404(Cow, pk=cow_id)
		frame = request.POST.get('frame')
		dairy_strength = request.POST.get('dairy_strength')
		udder = request.POST.get('udder')
		feet_legs = request.POST.get('feet_legs')
		stature = request.POST.get('stature')
		chest_width = request.POST.get('chest_width')
		body_depth = request.POST.get('body_depth')
		angularity = request.POST.get('angularity')
		cond_score = request.POST.get('cond_score')
		thurl_width = request.POST.get('thurl_width')
		rump_angle = request.POST.get('rump_angle')
		rump_width = request.POST.get('rump_width')
		right_legs_rv = request.POST.get('right_legs_rv')
		right_legs_sv = request.POST.get('right_legs_sv')
		foot_angle = request.POST.get('foot_angle')
		locomotion = request.POST.get('locomotion')
		cow_body_traits = CowBodyTraits(cow=referenced_cow, frame=frame, dairy_strength=dairy_strength, udder=udder, feet_legs=feet_legs, stature=stature, chest_width=chest_width, body_depth=body_depth, angularity=angularity, cond_score=cond_score, thurl_width=thurl_width, rump_angle=rump_angle, rump_width=rump_width, right_legs_rv=right_legs_rv,right_legs_sv=right_legs_sv, foot_angle=foot_angle, locomotion=locomotion)
		cow_body_traits.save()
		return HttpResponseRedirect(reverse("digitaldairy:cow_profile"))
	all_cows = Cow.objects.all()
	body_traits_list = CowBodyTraits.objects.all()
	context = {
		'all_cows': all_cows,
		'body_traits_list': body_traits_list,
	}
	return render(request, context=context, template_name='digitaldairy/html/cow-profile.html')


@login_required
@require_http_methods(['GET'])
def cow_milk_production_history(request):
	cow_id = request.GET.get('cow_id')
	referenced_cow = get_object_or_404(Cow, pk=cow_id)
	from_date_string = request.GET.get('from_date')
	to_date_string = request.GET.get('to_date')
	if from_date_string:
		try:
			from_date = datetime.datetime.strptime(from_date_string, '%Y-%m-%d')
		except ValueError:
			from_date = general_from_date
	else:
		from_date = general_from_date
	if to_date_string:
		try:
			to_date = datetime.datetime.strptime(to_date_string, '%Y-%m-%d')
		except ValueError:
			to_date = general_to_date
	else:
		to_date = general_to_date
	all_cows = Cow.objects.all()
	milk_production_list = MilkProductions.objects.filter(cow_id=referenced_cow) \
		.filter(milk_date__gte=from_date) \
		.filter(milk_date__lte=to_date)
	context = {
		'all_cows': all_cows,
		'from_date': from_date,
		'to_date': to_date,
		'referenced_cow': referenced_cow,
		'milk_production_list': milk_production_list
	}
	return render(request, context=context, template_name='digitaldairy/html/cow-milk-production-history.html')


@login_required
@require_http_methods(['POST'])
def save_milk_production(request):
	cow_id = request.POST['cow_id']
	milk_date = request.POST['milk_date']
	referenced_cow = get_object_or_404(Cow, pk=cow_id)
	am_quantity = request.POST.get('am_quantity')
	noon_quantity = request.POST.get('noon_quantity')
	pm_quantity = request.POST.get('pm_quantity')
	day_milk_production, created = MilkProductions.objects.update_or_create(milk_date=milk_date,
	cow_id= referenced_cow, defaults = {'am_quantity': am_quantity, 'noon_quantity':noon_quantity, 'pm_quantity': pm_quantity})
	request.session['milk_production_date'] = milk_date
	return  JsonResponse({
		'id': day_milk_production.id,
		'milk_date': day_milk_production.milk_date,
		'cow_id': day_milk_production.cow_id.id,
		'cow_name': day_milk_production.cow_id.name,
		'am_quantity': day_milk_production.am_quantity, 
		'noon_quantity': day_milk_production.noon_quantity,
		'pm_quantity': day_milk_production.pm_quantity,
		'milk_production_url': day_milk_production.cow_id.milk_production_history_url(),
		})


@login_required
@require_http_methods(['POST'])
def save_daily_milk_target(request):
	cow_id = request.POST['cow_id']
	referenced_cow = get_object_or_404(Cow, pk=cow_id)
	target_quantity = request.POST.get('milk_production_target')
	milk_production_target = MilkTargets()
	milk_production_target.cow_id = referenced_cow
	milk_production_target.target_quantity = target_quantity
	milk_production_target.save()
	return JsonResponse({
			'cow_id': milk_production_target.cow_id.id,
			'cow_name': milk_production_target.cow_id.name,
			'target_quantity': milk_production_target.target_quantity
			})


@login_required
@require_http_methods(['POST'])
def delete_day_milk_production(request):
	milk_production_date = request.POST.get('milk_production_date')
	milk_production_id = request.POST.get('milk_production_id')
	milk_production_to_delete = get_object_or_404(MilkProductions, id=milk_production_id)
	milk_production_to_delete.delete()
	return HttpResponseRedirect('/digitaldairy/daily_milk_production/?milk_production_date={0}'.format(milk_production_date))


@login_required
@require_http_methods(['POST'])
def delete_milk_production_target(request):
	cow_id = request.POST.get('cow_id')
	cow_with_milk_production_target = get_object_or_404(Cow, pk=cow_id)
	milk_production_target_to_delete = get_object_or_404(MilkTargets, pk=cow_with_milk_production_target)
	milk_production_target_to_delete.delete()
	return HttpResponseRedirect(reverse("digitaldairy:daily_milk_production"))


@login_required
@require_http_methods(['POST'])
def delete_milk_production_target(request):
	cow_id = request.POST.get('cow_id')
	referenced_cow = get_object_or_404(Cow, id=cow_id)
	milk_target_to_delete = get_object_or_404(MilkTargets, cow_id=referenced_cow)
	milk_target_to_delete.delete()
	return HttpResponseRedirect(reverse("digitaldairy:daily_milk_production"))


@login_required
@require_http_methods(['POST'])
def delete_calf_feeding(request):
	calf_feeding_id = request.POST.get('calf_feeding_id')
	calf_feeding = get_object_or_404(CalfFeeding, id=calf_feeding_id)
	calf_feeding.delete()
	return HttpResponseRedirect(reverse("digitaldairy:calf_management"))


@login_required
@require_http_methods(['GET'])
def clients_statements(request):
	sales_from_date = request.GET.get('sales_from_date')
	sales_to_date = request.GET.get('sales_to_date')
	client_id = request.GET.get('client_id')
	clients_list = Clients.objects.all()
	# set sales_from_date to default date if None else try to parse it
	if sales_from_date:
		try:
			sales_from_date = datetime.datetime.strptime(sales_from_date, '%Y-%m-%d')
		except:
			sales_from_date = general_from_date.replace(year=general_to_date.year, month= general_to_date.month)
	else:
		sales_from_date = general_from_date.replace(year= general_to_date.year, month= general_to_date.month)
	# set sales_to_date to general_to_date if None else try to parse it
	if sales_to_date:
		try:
			sales_to_date = datetime.datetime.strptime(sales_to_date, '%Y-%m-%d')
		except:
			sales_to_date = general_to_date
	else:
		sales_to_date = general_to_date
	if client_id:
		referenced_client = get_object_or_404(Clients, pk=client_id)
	else:
		referenced_client = clients_list[0] if clients_list.count() > 1 else None
	milk_sales_list = MilkSales.objects.filter(date__gte=sales_from_date, date__lte=sales_to_date,client=referenced_client)
	milk_sales_payments_list = MilkSalesPayments.objects.filter(milk_sale_date__gte=sales_from_date, milk_sale_date__lte=sales_to_date, client=referenced_client)
	total_sales_value = sum([milk_sale.quantity * milk_sale.unit_price for milk_sale in milk_sales_list])
	total_quantity_sold = sum([milk_sale.quantity for milk_sale in milk_sales_list])
	total_milk_sales_payments = sum([milk_sales_payment.amount_paid for milk_sales_payment in milk_sales_payments_list])
	milk_payments_balance = total_sales_value - total_milk_sales_payments
	context = {
		'total_milk_sales_payments': total_milk_sales_payments,
		'milk_payments_balance': milk_payments_balance,
		'total_sales_value': total_sales_value,
		'total_quantity_sold': total_quantity_sold,
		'sales_from_date': sales_from_date,
		'sales_to_date': sales_to_date,
		'milk_sales_list': milk_sales_list,
		'client': referenced_client,
		'clients_list': clients_list,
	}
	return render(request, context=context, template_name='digitaldairy/html/clients-statements.html')


@login_required
@require_http_methods(['GET'])
def consumers_statements(request):
	consumption_from_date = request.GET.get('consumption_from_date')
	consumption_to_date = request.GET.get('consumption_to_date')
	consumer_id = request.GET.get('consumer_id')
	referenced_consumer = 'All Consumers'
	consumers_list = Consumers.objects.all()
	# set consumption_from_date to default from_date if None else try to parse it
	if consumption_from_date:
		try:
			consumption_from_date= datetime.datetime.strptime(consumption_from_date, '%Y-%m-%d')
		except:
			sales_from_date = general_from_date.replace(year=general_to_date.year, month=general_to_date.month)
	else:
		consumption_from_date = general_from_date.replace(year=general_to_date.year, month= general_to_date.month)
	# set consumption_to_date to default to_date if None else try to parse it
	if consumption_to_date:
		try:
			consumption_to_date= datetime.datetime.strptime(consumption_to_date, '%Y-%m-%d')
		except:
			consumption_to_date = general_to_date
	else:
		consumption_to_date = general_to_date
	milk_consumption_list = MilkConsumptions.objects.filter(date__gte=consumption_from_date, date__lte=consumption_to_date)
	if consumer_id:
		referenced_consumer = get_object_or_404(Consumers, pk=consumer_id)
		milk_consumption_list = milk_consumption_list.filter(consumer=referenced_consumer)
	total_quantity_consumed = sum([milk_consumption.quantity for milk_consumption in milk_consumption_list])
	total_consumption_value = sum([milk_consumption.quantity * milk_consumption.consumer.unit_price  for milk_consumption in milk_consumption_list])
	context = {
		'total_consumption_value': total_consumption_value,
		'total_quantity_consumed' : total_quantity_consumed,
		'consumption_from_date': consumption_from_date,
		'consumption_to_date': consumption_to_date,
		'milk_consumption_list': milk_consumption_list,
		'consumer': referenced_consumer,
		'consumers_list': consumers_list,
	}
	return render(request, context=context, template_name='digitaldairy/html/consumers-statements.html')


@login_required
@require_http_methods(['GET'])
def get_clients_and_consumers(request):
	clients_list = Clients.objects.all()
	consumers_list = Consumers.objects.all()
	context = {
		'consumers_list': consumers_list,
		'clients_list': clients_list,
	}
	return render(request, context=context, template_name='digitaldairy/html/clients-consumers.html')


@login_required
@require_http_methods(['GET', 'POST'])
def get_employees(request):
	employees_list = Employees.objects.all()
	salaries_advances = salaries_and_advances.objects.all()
	context = {
		'employees_list': employees_list,
		'salaries_advances': salaries_advances,
	}
	if request.method == 'GET':
		return render(request, context=context, template_name='digitaldairy/html/employees-page.html')
	if request.method == 'POST':
		employee_name = request.POST.get("employee_name")
		employee_id = request.POST.get("employee_id")
		employee_contacts = request.POST.get("employee_contacts")
		date_hired = request.POST.get("date_hired")
		department = request.POST.get("department")
		designation = request.POST.get("designation")
		salary = request.POST.get("salary")
		employee_to_save = Employees()
		employee_to_save.name = employee_name
		employee_to_save.id = employee_id
		employee_to_save.contacts = employee_contacts
		employee_to_save.date_hired = date_hired
		employee_to_save.department = department
		employee_to_save.designation = designation
		employee_to_save.salary = salary
		employee_to_save.save()

		return render(request, context=context, template_name='digitaldairy/html/employees-page.html')


@login_required
@require_http_methods(['GET', 'POST'])
def cow_insurance(request):
	all_cows =  Cow.objects.all()
	insurance_list = []
	if request.method == 'GET':
		cow_id = request.GET.get('cow_id')
		if cow_id != None:
			referenced_cow = get_object_or_404(Cow, pk=cow_id)
			insurance_list = CowInsurance.objects.filter(cow=referenced_cow)
		else:
			insurance_list = CowInsurance.objects.all()
	else:
		#get information from the post object
		insurance_id = request.POST.get('insurance_id')
		from_date = request.POST.get('from_date')
		to_date = request.POST.get('to_date')
		cow_id = request.POST.get('cow_id')
		referenced_cow = get_object_or_404(Cow, pk=cow_id)
		premium_amount = request.POST.get('premium_amount')
		insured_value = request.POST.get('insured_value')
		insurance_policy = request.POST.get('insurance_policy')
		# add information to insurance instance
		insurance_to_save = CowInsurance()
		insurance_to_save.id = insurance_id
		insurance_to_save.from_date = from_date
		insurance_to_save.to_date = to_date
		insurance_to_save.cow = referenced_cow
		insurance_to_save.premium_amount = premium_amount
		insurance_to_save.insured_value = insured_value
		insurance_to_save.policy = insurance_policy
		# save the instance
		insurance_to_save.save()
		insurance_list = CowInsurance.objects.all()
	total_insurance_value = sum([insurance.insured_value for insurance in list(insurance_list)])
	context = {
		'total_insurance_value' : total_insurance_value,
		'insurance_list': insurance_list,
		'all_cows': all_cows
	}
	return render(request, context=context, template_name='digitaldairy/html/cow-insurance.html')



def getMonthIfNotNone(month):
	if month:
		try:
			month = int(month)
			month = month if month < 13 and month > 0 else general_to_date.month
		except:
			month = general_to_date.month
	else:
		month = general_to_date.month
	return month


def getYearIfNotNone(year):
	if year:
		try:
			year = int(year)
			year = year if year > 0 else general_to_date.year
		except:
			year = general_to_date.year
	else:
		year = general_to_date.year

	return year


@login_required
@require_http_methods(['GET'])
def income(request):
	income_month = request.GET.get('month') if request.GET.get('month') else request.session.get('month')
	income_year = request.GET.get('year') if request.GET.get('year') else request.session.get('year')
	income_month = getMonthIfNotNone(income_month)
	income_year = getYearIfNotNone(income_year)
	year_income_list = Income.objects.filter(date__year=income_year)
	month_income_list = year_income_list.filter(date__month=income_month)
	total_year_income = sum([ expense.amount for expense in year_income_list ])
	total_month_income = sum([ income.amount for income in month_income_list])
	income_chosen_date = datetime.date(income_year, income_month, 1)
	context = {
			'total_year_income': total_year_income,
			'total_month_income': total_month_income,
			'income_chosen_date': income_chosen_date,
			'income_list' : month_income_list,
		}
	return render(request, context=context, template_name='digitaldairy/html/income.html')


@login_required
@require_http_methods(['GET'])
def expenses(request):
	expenses_month = request.GET.get('month') if request.GET.get('month') else request.session.get('month')
	expenses_year = request.GET.get('year') if request.GET.get('year') else request.session.get('year')
	expenses_month = getMonthIfNotNone(expenses_month)
	expenses_year = getYearIfNotNone(expenses_year)
	expenses_chosen_date = datetime.date(expenses_year, expenses_month, 1)
	year_expenses_list = Expense.objects.filter(date__year=expenses_year)
	month_expenses_list = year_expenses_list.filter(date__month=expenses_month)
	total_year_expenses = sum([expense.amount for expense in year_expenses_list])
	total_month_expenses = sum([expense.amount for expense in month_expenses_list])
	context = {
			'total_year_expenses': total_year_expenses,
			'total_month_expenses': total_month_expenses,
			'expenses_chosen_date': expenses_chosen_date,
			'expenses_list': month_expenses_list,
		}
	return render(request, context=context, template_name='digitaldairy/html/expenses.html')


@login_required
@require_http_methods(['GET'])
def milk_sales(request):
	milk_sale_date = request.GET.get('milk_sale_date')if request.GET.get('milk_sale_date') else request.session.get('milk_sale_date')
	if milk_sale_date == None:
		milk_sale_date = general_to_date
	else:
		try:
			milk_sale_date = datetime.datetime.strptime(milk_sale_date, '%Y-%m-%d').date()
		except:
			milk_sale_date = general_to_date
	clients_list = Clients.objects.all()
	consumers_list = Consumers.objects.all()
	sales_list = MilkSales.objects.filter(date=milk_sale_date)
	total_sales = 0
	total_amount_of_money_from_sales = 0
	for sale in sales_list:
		total_sales += sale.quantity
		total_amount_of_money_from_sales += sale.quantity * sale.client.unit_price
	consumption_list = MilkConsumptions.objects.filter(date=milk_sale_date)
	total_consumption = 0
	for consumption in consumption_list:
		total_consumption += consumption.quantity
	context = {
		"milk_sale_date": milk_sale_date,
		'total_sales': total_sales,
		'total_amount_of_money_from_sales': total_amount_of_money_from_sales,
		'total_consumption': total_consumption,
		'consumers_list': consumers_list,
		'clients_list':clients_list,
		'sales_list': sales_list,
		'consumption_list': consumption_list,
	}
	return render(request, context=context, template_name='digitaldairy/html/milk-sales.html')


@login_required
@require_http_methods(['GET', 'POST'])
def milk_sales_payments(request):
	if request.method == 'GET':
		month = request.GET.get('month')
		year = request.GET.get('year')
		if year is None:
			year = request.session.get('year')
		if month is None:
			month = request.session.get('month')
		if year:
			try:
				year = int(year)
				year = 1 if year < 1 else year
			except ValueError:
				year = general_to_date.year
		else:
			year = general_to_date.year
		if month:
			try:
				month = int(month)
				month = 1 if (month > 12 or month < 1) else month
			except ValueError:
				month = general_to_date.month
		else:
			month = general_to_date.month
		selected_month_date = datetime.date(year=year, month=month, day=1)
		clients_list = Clients.objects.all()
		selected_month_milk_sales_list = MilkSales.objects.filter(date__month=month, date__year=year)
		milk_payments_list = MilkSalesPayments.objects.filter(date_of_payment__month=month, date_of_payment__year=year)
		client_id = request.GET.get('client_id')
		if client_id is None:
			client_id = request.session.get('client_id')
		if client_id != None:
			client = get_object_or_404(Clients, pk=client_id)
			milk_payments_list = milk_payments_list.filter(client=client)
			selected_month_milk_sales_list = selected_month_milk_sales_list.filter(client=client)
		else:
			client = 'All'
		total_milk_sales = sum([milk_sale.quantity * milk_sale.client.unit_price for milk_sale in list(selected_month_milk_sales_list)])
		total_quantity_sold = sum([milk_sale.quantity for milk_sale in list(selected_month_milk_sales_list)])
		total_amount_paid = sum([milk_payment.amount_paid for milk_payment in list(milk_payments_list)])
		balance = total_milk_sales - total_amount_paid
		context = {
			'client': client,
			'total_quantity_sold': total_quantity_sold,
			'total_amount_paid': total_amount_paid,
			'total_milk_sales': total_milk_sales,
			'balance': balance,
			'selected_month_date': selected_month_date,
			'milk_payments_list': milk_payments_list,
			'clients_list': clients_list
		}
		return render(request, context=context, template_name='digitaldairy/html/milk_sales_payments.html')
	elif request.method == 'POST':
		# get information from the post object
		milk_sales_payment_id = request.POST.get('milk_sale_payment_id')
		client_id = request.POST['client_id']
		referenced_client = get_object_or_404(Clients, pk=client_id)
		date_of_payment = request.POST.get('payment_date')
		milk_sale_date = request.POST.get('milk_sale_date')
		if milk_sale_date:
			try:
				milk_sale_date = datetime.datetime.strptime(milk_sale_date, '%Y-%m-%d')
			except ValueError:
				return
		else:
			return 
		amount_paid = request.POST.get('amount_paid')
		# add information to payment instance
		milk_sales_payment = MilkSalesPayments()
		milk_sales_payment.id = milk_sales_payment_id
		milk_sales_payment.date_of_payment = date_of_payment
		milk_sales_payment.milk_sale_date = milk_sale_date
		milk_sales_payment.client = referenced_client
		milk_sales_payment.amount_paid = amount_paid
		# save the instance
		milk_sales_payment.save()
		# save selected client in session
		request.session['client_id'] = referenced_client.id
		request.session['month'] = milk_sale_date.month
		request.session['year'] = milk_sale_date.year
		return HttpResponseRedirect(reverse("digitaldairy:milk_sales_payments"))


@login_required
@require_http_methods(['GET'])
def get_client_purchase_history(request, client_id):
	client = get_object_or_404(Clients, pk=client_id)
	sales_from_date = request.GET.get('sales_from_date')
	sales_to_date = request.GET.get('sales_to_date')
	if not sales_from_date:
		sales_from_date = general_from_date
	else:
		try:
			sales_from_date = datetime.datetime.strptime(sales_from_date, '%Y-%m-%d').date()
		except:
			messages.error(request, "Sales from date is in wrong format")
			return render(request, template_name="digitaldairy/html/client-purchase-history.html.html")
	if not sales_to_date:
		sales_to_date = general_to_date
	else:
		try:
			sales_to_date = datetime.datetime.strptime(sales_to_date, '%Y-%m-%d').date()
		except:
			messages.error(request, "Sales to date is in wrong format")
			return render(request, template_name="digitaldairy/html/client-purchase-history.html.html")
	milk_sales_list = MilkSales.objects.filter(client=client) \
		.filter(date__gte=sales_from_date).filter(date__lte=sales_to_date)
	context = {
		'client': client,
		'sales_from_date': sales_from_date,
		'sales_to_date': sales_to_date,
		'milk_sales_list': milk_sales_list
	}
	return render(request, context=context, template_name="digitaldairy/html/client-purchase-history.html")


@login_required
@require_http_methods(['GET'])
def get_consumer_consumption_history(request, consumer_id):
	consumer = get_object_or_404(Consumers, pk=consumer_id)
	consumption_from_date = request.GET.get('consumption_from_date')
	consumption_to_date = request.GET.get('consumption_to_date')
	if not consumption_from_date:
		consumption_from_date = general_from_date
	else:
		try:
			consumption_from_date = datetime.datetime.strptime(consumption_from_date, '%Y-%m-%d').date()
		except:
			messages.error(request, "Consumption from date is in wrong format")
			return render(request, template_name="digitaldairy/html/consumer-consumption-history.html")
	if not consumption_to_date:
		consumption_to_date = general_to_date
	else:
		try:
			consumption_to_date = datetime.datetime.strptime(consumption_to_date, '%Y-%m-%d').date()
		except:
			messages.error(request, "Consumption to date is in wrong format")
			return render(request, template_name="digitaldairy/html/consumer-consumption-history.html")
	milk_consumption_list = MilkConsumptions.objects.filter(consumer=consumer) \
			.filter(date__gte=consumption_from_date) \
			.filter(date__lte=consumption_to_date)
	context = {
		'consumer': consumer,
		'consumption_from_date': consumption_from_date,
		'consumption_to_date': consumption_to_date,
		'milk_consumption_list':milk_consumption_list
	}
	return render(request, context=context, template_name="digitaldairy/html/consumer-consumption-history.html")


@login_required
@require_http_methods(['POST'])
def save_milk_sale(request):
	client_id = request.POST['client_id']
	sale_date = request.POST.get('sale_date')
	quantity = request.POST.get('sale_quantity')
	client = get_object_or_404(Clients, pk=client_id)
	_milk_sale_to_save, _created = MilkSales.objects.update_or_create(client=client,date=sale_date,defaults={'quantity': quantity, 'unit_price': client.unit_price})
	# save milk_sale_date in session
	request.session['milk_sale_date'] = sale_date
	return HttpResponseRedirect(reverse('digitaldairy:milk_sales'))


@login_required
@require_http_methods(['POST'])
def save_cow_sale(request):
	cow_id = request.POST['cow_id']
	sale_date = request.POST['sale_date']
	cow_value = request.POST['cow_value']
	client_name = request.POST.get('client_name')
	sale_remarks = request.POST.get('sale_remarks')
	referenced_cow = get_object_or_404(Cow, pk=cow_id)
	created_record, created = CowSales.objects \
		.update_or_create(cow=referenced_cow, defaults={
		'date': sale_date,
		'cow_value': cow_value,
		'client_name': client_name,
		'sale_remarks': sale_remarks,
	})
	return HttpResponseRedirect(reverse('digitaldairy:cow_sales'))


@login_required
@require_http_methods(['POST'])
def save_daily_feeding(request):
	daily_feeding_id = request.POST.get('daily_feeding_id')
	feed_formulation_id = request.POST.get('feed_formulation')
	feed_formulation = get_object_or_404(FeedFormulation, pk=feed_formulation_id)
	feeding_date = request.POST.get('feeding_date')
	feeding_category = request.POST.get('feeding_category')
	feed_formulation_quantity = request.POST.get('feed_formulation_quantity')
	daily_feeding_record = DailyFeeding()
	daily_feeding_record.id = daily_feeding_id
	daily_feeding_record.feed_formulation = feed_formulation
	daily_feeding_record.date = feeding_date
	daily_feeding_record.feeding_category = feeding_category
	daily_feeding_record.quantity = feed_formulation_quantity
	daily_feeding_record.save()
	return HttpResponseRedirect(reverse('digitaldairy:daily_feeding'))


@login_required
@require_http_methods(['POST'])
def save_feed_item(request):
	feed_item_name = request.POST['item_name']
	item_unit_measure = request.POST.get('item_unit_measure')
	item_unit_price = request.POST.get('item_unit_price')
	item_available_stock = request.POST.get('item_available_stock')
	item_reorder_level = request.POST.get('item_reorder_level')
	feed_item_record = FeedItems()
	feed_item_record.name = feed_item_name
	feed_item_record.unit_of_measure = item_unit_measure
	feed_item_record.unit_price = item_unit_price
	feed_item_record.initial_stock = item_available_stock
	feed_item_record.available_stock = item_available_stock
	feed_item_record.reorder_level = item_reorder_level
	feed_item_record.save()
	return HttpResponseRedirect(reverse('digitaldairy:cow_feed_items'))


@login_required
@require_http_methods(['POST'])
def save_feed_formulation(request):
	feed_formulation_id = request.POST.get('feed_formulation_id')
	feed_formulation_name = request.POST.get('feed_formulation_name')
	feed_formulation_quantity = request.POST.get('feed_formulation_quantity')
	feed_item_name = request.POST.get('feed_item')
	feed_item = get_object_or_404(FeedItems, pk=feed_item_name)
	feed_formulation_part_quantity = request.POST.get('feed_formulation_part_quantity')
	# create and save feed formulation instance
	feed_formulation, _created = FeedFormulation.objects.update_or_create(name=feed_formulation_name, defaults={'quantity': feed_formulation_quantity})
	# create feed formulation part to refer to feed formulation
	feed_formulation_part, _created = FeedFormulationPart.objects.update_or_create(feed_item=feed_item,feed_formulation=feed_formulation, defaults={
		'quantity': feed_formulation_part_quantity})
	return HttpResponseRedirect(reverse('digitaldairy:cow_feeds'))


@login_required
@require_http_methods(['POST'])
def save_feed_formulation_part(request):
	feed_form_part_id = request.POST['feed_form_part_id']
	feed_formulation_part_quantity = request.POST.get('feed_form_part_quantity')
	# create and save feed formulation instance
	_feed_formulation_part, _created = FeedFormulationPart.objects.update_or_create(id=feed_form_part_id, defaults={
		'quantity': feed_formulation_part_quantity})
	return JsonResponse({
			'id': _feed_formulation_part.id,
			'name': _feed_formulation_part.feed_item.name,
			'quantity': _feed_formulation_part.quantity,
			})


@login_required
@require_http_methods(['POST'])
def save_milk_consumption(request):
	milk_consumption_id = request.POST.get('milk_consumption_id')
	consumer_name = request.POST.get('consumer_id')
	consumer = get_object_or_404(Consumers, pk=consumer_name)
	quantity = request.POST.get('consumed_quantity')
	consumption_date = request.POST.get('consumption_date')
	_milk_consumption_to_save, _created = MilkConsumptions.objects.update_or_create(consumer=consumer, date=consumption_date, defaults={'quantity': quantity})
	request.session['milk_sale_date'] = consumption_date
	return HttpResponseRedirect(reverse('digitaldairy:milk_sales'))


@login_required
@require_http_methods(['POST'])
def save_client(request):
	client_id = request.POST.get('client_id')
	client_name = request.POST['client_name']
	client_contacts = request.POST.get('client_contacts')
	client_location = request.POST.get('client_location')
	client_unit_price = request.POST['client_unit_price']
	client = Clients()
	client.id = client_id
	client.name = client_name
	client.contacts = client_contacts
	client.location = client_location
	client.unit_price = client_unit_price
	client.save()
	return HttpResponseRedirect(reverse('digitaldairy:clients_consumers'))


@login_required
@require_http_methods(['POST'])
def save_cow_treatment_record(request):
	treatment_id = request.POST.get('treatment_id')
	cow_id = request.POST.get('cow_id')
	referenced_cow = get_object_or_404(Cow, pk=cow_id)
	treatment_date = request.POST.get('treatment_date')
	disease = request.POST.get('disease')
	diagnosis = request.POST.get('diagnosis')
	treatment_cost = request.POST.get('treatment_cost')
	treatment = request.POST.get('treatment')
	vet_name = request.POST.get('vet_name')
	treatment_record = TreatmentRecords(id=treatment_id,
		cow=referenced_cow, date=treatment_date, treatment_cost=treatment_cost, disease=disease, diagnosis=diagnosis, treatment=treatment, vet_name=vet_name)
	treatment_record.save()
	return HttpResponseRedirect(reverse('digitaldairy:cow_health'))


@login_required
@require_http_methods(['POST'])
def save_cow_deworming_record(request):
	deworming_id = request.POST.get('deworming_id')
	cow_id = request.POST.get('cow_id')
	referenced_cow = get_object_or_404(Cow, pk=cow_id)
	deworming_date = request.POST.get('deworming_date')
	dewormer = request.POST.get('dewormer')
	deworming_cost = request.POST.get('deworming_cost')
	next_deworming_date = request.POST.get('next_deworming_date')
	created_record, created = Deworming.objects \
		.update_or_create(id=deworming_id, defaults={
		'cow': referenced_cow,
		'deworming_date' : deworming_date,
		'dewormer': dewormer,
		'deworming_cost': deworming_cost,
		'next_deworming_date' : next_deworming_date
	})
	return HttpResponseRedirect(reverse('digitaldairy:deworming'))


@login_required
@require_http_methods(['POST'])
def save_cow_vaccination_record(request):
	vaccination_id = request.POST.get('vaccination_id')
	cow_id = request.POST['cow_id']
	print(cow_id)
	referenced_cow = get_object_or_404(Cow, pk=cow_id)
	vaccination_date = request.POST['vaccination_date']
	vaccine = request.POST.get('vaccine')
	vaccination_cost = request.POST.get('vaccination_cost')
	next_vaccination_date = request.POST.get('next_vaccination_date')
	created_record, created = Vaccinations.objects \
		.update_or_create(id=vaccination_id, defaults={
		'cow': referenced_cow,
		'vaccination_date': vaccination_date,
		'vaccine': vaccine,
		'vaccination_cost': vaccination_cost,
		'next_vaccination_date' : next_vaccination_date
	})
	return HttpResponseRedirect(reverse('digitaldairy:vaccinations'))


@login_required
@require_http_methods(['POST'])
def save_cow_death_record(request):
	cow_id = request.POST['cow_id']
	referenced_cow = get_object_or_404(Cow, pk=cow_id)
	death_date = request.POST['death_date']
	autopsy_date = request.POST.get('autopsy_date')
	death_cause = request.POST.get('death_cause')
	referenced_cow.status = 'Inactive'
	created_record, created = Deaths.objects \
		.update_or_create(cow=referenced_cow, defaults={
		'death_date': death_date,
		'autopsy_date': autopsy_date,
		'death_cause': death_cause,
	})
	return HttpResponseRedirect(reverse('digitaldairy:deaths_autopsy'))


@login_required
@require_http_methods(['POST'])
def save_cow_disease_record(request):
	disease_id = request.POST.get('disease_id')
	date_discovered = request.POST.get('date_discovered')
	disease_name = request.POST.get('disease_name')
	disease_details = request.POST.get('disease_details')
	disease = Diseases()
	disease.id = disease_id
	disease.date_discovered = date_discovered
	disease.name = disease_name
	disease.details = disease_details
	disease.save()
	return HttpResponseRedirect(reverse('digitaldairy:cow_diseases'))


@login_required
@require_http_methods(['POST'])
def save_semen_catalog(request):
	semen_catalog_id = request.POST.get('semen_catalog_id')
	bull_code = request.POST['bull_code']
	bull_name = request.POST.get('bull_name')
	bull_breed = request.POST.get('bull_breed')
	num_of_straws = request.POST.get('num_of_straws')
	cost_per_straw = request.POST.get('cost_per_straw')
	company_name = request.POST.get('company_name')
	semen_catalog = SemenRecords()
	semen_catalog.id = semen_catalog_id
	semen_catalog.bull_code = bull_code
	semen_catalog.bull_name = bull_name if bull_name else bull_code
	semen_catalog.bull_breed = bull_breed
	semen_catalog.num_of_straws = num_of_straws
	semen_catalog.cost_per_straw = cost_per_straw
	semen_catalog.company_name = company_name
	semen_catalog.save()
	return HttpResponseRedirect(reverse('digitaldairy:semen_catalog'))


@login_required
@require_http_methods(['POST'])
def save_income(request):
	income_id = request.POST.get('income_id')
	income_date = request.POST.get('income_date')
	if not income_date:
		messages.error(request, 'Date not available!')
		return render(request, template_name='digitaldairy/html/income.html')
	else:
		try:
			income_date = datetime.datetime.strptime(income_date, '%Y-%m-%d').date()
		except:
			messages.error(request, 'Date is in wrong format.')
			messages.error(request, 'Please give a correct date in the format yyyy-mm-dd')
			return render(request, template_name='digitaldairy/html/income.html')
	income_amount = request.POST.get('income_amount')
	income_source = request.POST.get('income_source')
	income = Income()
	income.id = income_id
	income.date = income_date
	income.amount = income_amount
	income.source = income_source
	income.save()
	# add year and month to the session
	request.session['year'] = income_date.year
	request.session['month'] = income_date.month
	return HttpResponseRedirect(reverse("digitaldairy:income"))


@login_required
@require_http_methods(['POST'])
def save_expense(request):
	expense_id = request.POST['expense_id']
	expense_date = request.POST['expense_date']
	if not expense_date:
		messages.error(request, 'Date is not available')
		return render(request, template_name='digitaldairy/html/expenses.html')
	else:
		try:
			expense_date = datetime.datetime.strptime(expense_date, '%Y-%m-%d').date()
		except:
			messages.error(request, 'Expenses date is in wrong format.')
			messages.error(request, 'Please give a correct date in the format yyyy-mm-dd')
			return render(request, template_name='digitaldairy/html/expenses.html')
	expense_amount = request.POST['expense_amount']
	expense_source = request.POST.get('expense_source')
	expense = Expense()
	expense.id = expense_id
	expense.date = expense_date
	expense.amount = expense_amount
	expense.source = expense_source
	expense.save()
	# add the year and month to the session
	request.session['month'] = expense_date.year
	request.session['month'] = expense_date.month
	return HttpResponseRedirect(reverse('digitaldairy:expenses'))


@login_required
@require_http_methods(['POST'])
def save_cow(request):
	cow_id = request.POST.get('cow_id')
	date_of_birth = request.POST.get('date_of_birth')
	color = request.POST.get('color')
	lactations = request.POST.get('lactations')
	cow_name = request.POST.get('cow_name')
	grade = request.POST.get('grade')
	group = request.POST.get('group')
	birth_weight = request.POST.get('birth_weight')
	breed = request.POST.get('breed')
	sire_id = request.POST.get('sire_id').strip()
	dam_id = request.POST.get('dam')
	category = request.POST.get('category')
	source = request.POST.get('source')
	cow_to_save = Cow(id=cow_id, group=group, name=cow_name, birth_weight=birth_weight, breed=breed, dob=date_of_birth, grade=grade, source= source, lactations=lactations, category=category, color=color)
	if dam_id:
		dam = get_object_or_404(Cow, pk=dam_id)
		cow_to_save.dam = dam
	if sire_id:
		sire = get_object_or_404(SemenRecords, bull_code=sire_id)
		cow_to_save.sire = sire
	cow_to_save.save()
	return HttpResponseRedirect(reverse('digitaldairy:cows'))


@login_required
@require_http_methods(['POST'])
def save_calf(request):
	cow_id = request.POST.get('cow_id')
	date_of_birth = request.POST.get('date_of_birth')
	color = request.POST.get('color')
	lactations = request.POST.get('lactations')
	cow_name = request.POST.get('cow_name')
	grade = request.POST.get('grade')
	group = request.POST.get('group')
	birth_weight = request.POST.get('birth_weight')
	breed = request.POST.get('breed')
	sire_id = request.POST.get('sire')
	sire = None
	if sire_id:
		sire = get_object_or_404(SemenRecords,pk=sire_id)
	dam_id = request.POST.get('dam')
	dam = None
	if dam_id:
		dam = get_object_or_404(Cow, pk=dam_id)
	category = request.POST.get('category')
	cow_to_save = Cow(id=cow_id, group=group, name=cow_name, birth_weight=birth_weight, sire=sire, dam=dam, breed=breed, dob=date_of_birth, grade=grade, lactations=lactations, category=category, color=color)
	cow_to_save.save()
	return HttpResponseRedirect(reverse("digitaldairy:cows"))


@login_required
@require_http_methods(['POST'])
def save_cow_autopsy_record(request):
	death_record_id = request.POST['death_record_id']
	death_record =  get_object_or_404(Deaths, pk=death_record_id)
	autopsy_date = request.POST.get('autopsy_date')
	autopsy_results = request.POST.get('autopsy_results')
	autopsy_cost = request.POST.get('autopsy_cost')
	vet_name = request.POST.get('vet_name')
	death_record.autopsy_date = autopsy_date
	death_record.autopsy_results =  autopsy_results
	death_record.autopsy_cost = autopsy_cost
	death_record.vet_name = vet_name
	death_record.save()
	return HttpResponseRedirect(reverse("digitaldairy:deaths_autopsy"))


@login_required
@require_http_methods(['POST'])
def save_cow_ai_record(request):
	ai_record_id = request.POST.get('ai_record_id')
	cow_id = request.POST.get('cow_id')
	service_date = request.POST.get('service_date')
	if service_date:
		try:
			service_date = datetime.datetime.strptime(service_date, '%Y-%m-%d')
		except:
			return ''
	else:
		return ''
	bull_code = request.POST.get('bull_code')
	semen_record = get_object_or_404(SemenRecords, bull_code=bull_code)
	vet_name = request.POST.get('vet_name')
	ai_cost = request.POST.get('ai_cost')
	open_days = request.POST.get('open_days')
	inbreeding_status = request.POST.get('inbreeding_status')
	if ai_record_id:
		ai_record = get_object_or_404(AiRecords, pk=ai_record_id)
		ai_record.inbreeding = inbreeding_status
		ai_record.open_days = open_days
		ai_record.ai_cost = ai_cost
		ai_record.service_date = service_date
		ai_record.first_heat_check_date = service_date + dateutil.relativedelta.relativedelta(days=21)
		ai_record.second_heat_check_date = ai_record.first_heat_check_date + dateutil.relativedelta.relativedelta(days=21)
		ai_record.pregnancy_check_date = service_date + dateutil.relativedelta.relativedelta(months=3)
		ai_record.drying_date = service_date + dateutil.relativedelta.relativedelta(months=7)
		ai_record.steaming_date = service_date + dateutil.relativedelta.relativedelta(months=8)
		ai_record.due_date = service_date + dateutil.relativedelta.relativedelta(months=9)
		ai_record.semen_record = semen_record
		# the cow being referenced is not being changed here
		# ai_record.cow = referenced_cow
		ai_record.vet_name = vet_name
		ai_record.cost = ai_cost
		ai_record.save()
	else:
		ai_record = AiRecords()
		referenced_cow = get_object_or_404(Cow, pk=cow_id)
		ai_record.service_date = service_date
		ai_record.first_heat_check_date = ai_record.service_date +  dateutil.relativedelta.relativedelta(days=21)
		ai_record.second_heat_check_date = ai_record.first_heat_check_date +  dateutil.relativedelta.relativedelta(days=21)
		ai_record.pregnancy_check_date = ai_record.service_date +  dateutil.relativedelta.relativedelta(months=3)
		ai_record.drying_date =  ai_record.service_date +  dateutil.relativedelta.relativedelta(months=7)
		ai_record.steaming_date = ai_record.service_date +  dateutil.relativedelta.relativedelta(months=8)
		ai_record.due_date =  ai_record.service_date +  dateutil.relativedelta.relativedelta(months=9)
		ai_record.semen_record = semen_record
		ai_record.cow = referenced_cow
		ai_record.vet_name = vet_name
		ai_record.cost = ai_cost
		ai_record.save()
	return HttpResponseRedirect(reverse("digitaldairy:ai_records"))


@login_required
@require_http_methods(['POST'])
def save_calving_record(request):
	ai_record_id = request.POST.get('ai_record_id')
	# get the ai_record associated with this calving
	ai_record = get_object_or_404(AiRecords, pk=ai_record_id)
	# get additional attributes of the calving instance
	calf_code = request.POST.get('calf_code')
	calf_name = request.POST.get('calf_name')
	calving_date = request.POST.get('calving_date')
	calf_sex = request.POST.get('calf_sex')
	calving_type = request.POST.get('calving_type')
	calf_breed = request.POST.get('calf_breed')
	calf_color = request.POST.get('calf_color')
	calf_weight = request.POST.get('calf_weight')
	# build instance of cow to save
	cow_to_save = Cow()
	cow_to_save.dam = ai_record.cow
	cow_to_save.sire = ai_record.semen_record
	cow_to_save.id = calf_code
	cow_to_save.name = calf_name
	cow_to_save.dob = calving_date
	cow_to_save.category = calf_sex
	cow_to_save.breed = calf_breed
	cow_to_save.color = calf_color
	cow_to_save.birth_weight = calf_weight
	cow_to_save.save()
	# build calving instance to save
	calving_to_save = Calvings()
	calving_to_save.ai_record = ai_record
	calving_to_save.calf = cow_to_save
	calving_to_save.calving_date = calving_date
	calving_to_save.calving_type = calving_type
	calving_to_save.save()
	# change ai-record calving status to Calved and save
	ai_record.calving_status = 'Calved'
	ai_record.save()
	return HttpResponseRedirect(reverse("digitaldairy:calving_maternity"))


@login_required
@require_http_methods(['POST'])
def save_abortion_miscarriage_record(request):
	ai_record_id = request.POST.get('ai_record_id')
	# get the ai_record associated with this abortion
	ai_record = get_object_or_404(AiRecords, pk=ai_record_id)
	# get additional attributes of the abortion/miscarriage instance
	event_date = request.POST.get('event_date')
	event_type = request.POST.get('event_type')
	event_cause = request.POST.get('event_cause')
	event_cost = request.POST.get('event_cost')
	vet_name = request.POST.get('vet_name')
	ai_record.calving_status = "Aborted" if event_cause == "Abortion"  else "Miscarriaged"
	ai_record.save()
	# build instance of abortion/miscarriage to save
	abortion_miscarriage_to_save = AbortionMiscarriages()
	abortion_miscarriage_to_save.ai_record = ai_record
	abortion_miscarriage_to_save.date = event_date
	abortion_miscarriage_to_save.type = event_type
	abortion_miscarriage_to_save.cause = event_cause
	abortion_miscarriage_to_save.cost = event_cost
	abortion_miscarriage_to_save.vet_name = vet_name
	# save instance to the database
	abortion_miscarriage_to_save.save()
	return HttpResponseRedirect(reverse("digitaldairy:abortions_miscarriages"))


@login_required
@require_http_methods(['POST'])
def save_pregnancy_diagnosis(request):
	ai_record_id = request.POST.get('ai_record_id')
	ai_record = get_object_or_404(AiRecords, pk=ai_record_id)
	pregnancy_diagnosis_date = request.POST.get('pregnancy_diagnosis_date')
	pregnancy_diagnosis_result = request.POST.get('pregnancy_diagnosis_result')
	pregnancy_diagnosis_cost = request.POST.get('pregnancy_diagnosis_cost')
	pregnancy_diagnosis_vet_name = request.POST.get('pregnancy_diagnosis_vet_name')
	ai_record.pregnancy_diagnosis_date = pregnancy_diagnosis_date
	ai_record.pregnancy_diagnosis_result = pregnancy_diagnosis_result
	ai_record.pregnancy_diagnosis_cost = pregnancy_diagnosis_cost
	ai_record.pregnancy_diagnosis_vet_name = pregnancy_diagnosis_vet_name
	ai_record.save()

	return HttpResponseRedirect(reverse('digitaldairy:pregnancy_diagnosis'))


@login_required
@require_http_methods(['POST'])
def save_pregnancy_calendar(request):
	ai_record_id = request.POST.get('ai_record_id')
	ai_record = get_object_or_404(AiRecords, pk=ai_record_id)
	first_heat_check_date = request.POST.get('first_heat_check_date')
	second_heat_check_date = request.POST.get('second_heat_check_date')
	pregnancy_diagnosis_date = request.POST.get('pregnancy_diagnosis_date')
	drying_date = request.POST.get('drying_date')
	steaming_date = request.POST.get('steaming_date')
	due_date = request.POST.get('due_date')
	ai_record.first_heat_check_date = first_heat_check_date
	ai_record.second_heat_check_date = second_heat_check_date
	ai_record.pregnancy_diagnosis_date = pregnancy_diagnosis_date
	ai_record.drying_date = drying_date
	ai_record.steaming_date = steaming_date
	ai_record.due_date = due_date
	ai_record.save()
	return HttpResponseRedirect(reverse('digitaldairy:pregnancy_diagnosis'))


@login_required
@require_http_methods(['POST'])
def save_consumer(request):
	consumer_id = request.POST.get('consumer_id')
	consumer_name = request.POST['consumer_name']
	consumer_contacts = request.POST.get('consumer_contacts')
	consumer_location = request.POST.get('consumer_location')
	consumer = Consumers()
	consumer.id = consumer_id
	consumer.name = consumer_name
	consumer.contacts = consumer_contacts
	consumer.location = consumer_location
	consumer.save()
	return HttpResponseRedirect(reverse("digitaldairy:clients_consumers"))


@login_required
@require_http_methods(['POST'])
def delete_consumer(request):
	consumer_id = request.POST.get('consumer_id')
	consumer_to_delete = get_object_or_404(Consumers, pk=consumer_id)
	consumer_to_delete.delete()
	return HttpResponseRedirect(reverse("digitaldairy:clients_consumers"))


@login_required
@require_http_methods(['POST'])
def delete_employee(request):
	employee_id = request.POST['employee_id']
	employee_to_delete = get_object_or_404(Employees, pk=employee_id)
	employee_to_delete.delete()
	return HttpResponseRedirect(reverse("digitaldairy:employees"))


@login_required
@require_http_methods(['POST'])
def delete_milk_consumption(request):
	milk_consumption_id = request.POST['milk_consumption_id']
	milk_consumption_to_delete = get_object_or_404(MilkConsumptions, pk=milk_consumption_id)
	milk_consumption_to_delete.delete()
	return HttpResponseRedirect(reverse("digitaldairy:milk_sales"))


@login_required
@require_http_methods(['POST'])
def delete_milk_sale(request):
	milk_sale_id = request.POST['milk_sale_id']
	milk_sale_to_delete = get_object_or_404(MilkSales, pk=milk_sale_id)
	milk_sale_to_delete.delete()
	return HttpResponseRedirect(reverse("digitaldairy:milk_sales"))


@login_required
@require_http_methods(['POST'])
def delete_milk_sale_payment(request):
	milk_sale_payment_id = request.POST['milk_sale_payment_id']
	milk_sale_payment = get_object_or_404(MilkSalesPayments, pk=milk_sale_payment_id)
	milk_sale_payment.delete()
	return HttpResponseRedirect(reverse("digitaldairy:milk_sales_payments"))


@login_required
@require_http_methods(['POST'])
def delete_income(request):
	income_id = request.POST['income_id']
	income = get_object_or_404(Income, pk=income_id)
	income.delete()
	return HttpResponseRedirect(reverse("digitaldairy:income"))


@login_required
@require_http_methods(['POST'])
def delete_vaccination(request):
	vaccination_id = request.POST['vaccination_id']
	vaccination = get_object_or_404(Vaccinations, pk=vaccination_id)
	vaccination.delete()
	return HttpResponseRedirect(reverse("digitaldairy:vaccinations"))


@login_required
@require_http_methods(['POST'])
def delete_deworming(request):
	deworming_id = request.POST['deworming_id']
	deworming = get_object_or_404(Deworming, pk=deworming_id)
	deworming.delete()
	return HttpResponseRedirect(reverse("digitaldairy:deworming"))


@login_required
@require_http_methods(['POST'])
def delete_semen_catalog(request):
	semen_catalog_id = request.POST['semen_catalog_id']
	semen_catalog = get_object_or_404(SemenRecords, pk=semen_catalog_id)
	semen_catalog.delete()
	return HttpResponseRedirect(reverse("digitaldairy:semen_catalog"))


@login_required
@require_http_methods(['POST'])
def delete_cow_disease(request):
	disease_id = request.POST['disease_id']
	disease = get_object_or_404(Diseases, pk=disease_id)
	disease.delete()
	return HttpResponseRedirect(reverse("digitaldairy:cow_diseases"))


@login_required
@require_http_methods(['POST'])
def delete_treatment(request):
	treatment_id = request.POST['treatment_id']
	treatment = get_object_or_404(TreatmentRecords, pk=treatment_id)
	treatment.delete()
	return HttpResponseRedirect(reverse("digitaldairy:cow_health"))


@login_required
@require_http_methods(['POST'])
def delete_weight(request):
	weight_id = request.POST['weight_id']
	weight = get_object_or_404(WeightRecords, pk=weight_id)
	weight.delete()
	return HttpResponseRedirect(reverse("digitaldairy:weight_recording"))


@login_required
@require_http_methods(['POST'])
def delete_feed_item(request):
	feed_name = request.POST['feed_item_name']
	feed_item = get_object_or_404(FeedItems, pk=feed_name)
	feed_item.delete()
	return HttpResponseRedirect(reverse("digitaldairy:cow_feed_items"))


@login_required
@require_http_methods(['POST'])
def delete_feed_formulation(request):
	feed_formulation_id = request.POST['feed_formulation_id']
	feed_formulation = get_object_or_404(FeedFormulation, pk=feed_formulation_id)
	feed_formulation.delete()
	return HttpResponseRedirect(reverse("digitaldairy:cow_feeds"))


@login_required
@require_http_methods(['POST'])
def delete_daily_feeding(request):
	daily_feeding_id = request.POST['daily_feeding_id']
	daily_feeding = get_object_or_404(DailyFeeding, pk=daily_feeding_id)
	daily_feeding.delete()
	return HttpResponseRedirect(reverse("digitaldairy:daily_feeding"))


@login_required
@require_http_methods(['POST'])
def delete_feeding_programme(request):
	feeding_programme_id = request.POST['feeding_programme_id']
	feeding_programme = get_object_or_404(FeedingProgramme, pk=feeding_programme_id)
	feeding_programme.delete()
	return HttpResponseRedirect(reverse("digitaldairy:cow_feeds"))

@login_required
@require_http_methods(['POST'])
def delete_feed_formulation_part(request):
	feed_formulation_part_id = request.POST['feed_formulation_part_id']
	feed_formulation_part = get_object_or_404(FeedFormulationPart, pk=feed_formulation_part_id)
	feed_formulation_part.delete()
	return HttpResponseRedirect(reverse("digitaldairy:cow_feeds"))

@login_required
@require_http_methods(['POST'])
def delete_expense(request):
	expense_id = request.POST['expense_id']
	expense = get_object_or_404(Expense, pk=expense_id)
	expense.delete()
	return HttpResponseRedirect(reverse("digitaldairy:expenses"))


@login_required
@require_http_methods(['POST'])
def delete_cow_sale(request):
	cow_id = request.POST['cow_id']
	cow_sale_to_delete = get_object_or_404(CowSales, pk=cow_id)
	cow_sale_to_delete.delete()
	return HttpResponseRedirect(reverse("digitaldairy:cow_sales"))


@login_required
@require_http_methods(['POST'])
def delete_cow(request):
	cow_id = request.POST['cow_id']
	cow_to_delete = get_object_or_404(Cow, pk=cow_id)
	cow_to_delete.delete()
	return HttpResponseRedirect(reverse("digitaldairy:cows"))


@login_required
@require_http_methods(['POST'])
def delete_cow_body_traits(request):
	body_traits_id = request.POST['body_traits_id']
	body_traits_to_delete = get_object_or_404(CowBodyTraits, pk=body_traits_id)
	body_traits_to_delete.delete()
	return HttpResponseRedirect(reverse("digitaldairy:cow_profile"))


@login_required
@require_http_methods(['POST'])
def delete_cow_death(request):
	cow_id = request.POST.get('cow_id')
	cow_death_to_delete = get_object_or_404(Deaths, pk=cow_id)
	cow_death_to_delete.delete()
	return HttpResponseRedirect(reverse("digitaldairy:deaths_autopsy"))


@login_required
@require_http_methods(['POST'])
def delete_cow_death_autopsy(request):
	cow_id = request.POST.get('cow_id')
	cow_death_to_delete = get_object_or_404(Deaths, pk=cow_id)
	cow_death_to_delete.autopsy_date = None
	cow_death_to_delete.autopsy_results = ''
	cow_death_to_delete.autopsy_cost = 0
	return HttpResponseRedirect(reverse("digitaldairy:deaths_autopsy"))


@login_required
@require_http_methods(['POST'])
def delete_client(request):
	client_id = request.POST.get('client_id')
	client_to_delete = get_object_or_404(Clients, pk=client_id)
	client_to_delete.delete()
	return HttpResponseRedirect(reverse("digitaldairy:clients_consumers"))


@login_required
@require_http_methods(['POST'])
def delete_pregnancy_diagnosis(request):
	ai_record_id = request.POST.get('ai_record_id')
	ai_record = get_object_or_404(AiRecords, pk=ai_record_id)
	ai_record.pregnancy_diagnosis_date = None
	ai_record.pregnancy_diagnosis_result = 'Unconfirmed'
	ai_record.pregnancy_diagnosis_cost = 0
	ai_record.pregnancy_diagnosis_vet_name = ''
	ai_record.save()
	return HttpResponseRedirect(reverse("digitaldairy:pregnancy_diagnosis"))


@login_required
@require_http_methods(['POST'])
def delete_ai_record(request):
	ai_record_id = request.POST.get('ai_record_id')
	ai_record = get_object_or_404(AiRecords, pk=ai_record_id)
	ai_record.delete()
	return HttpResponseRedirect(reverse("digitaldairy:ai_records"))


@login_required
@require_http_methods(['POST'])
def delete_calving(request):
	calving_id = request.POST.get('calving_id')
	calving = get_object_or_404(Calvings, pk=calving_id)
	calving.delete()
	return HttpResponseRedirect(reverse("digitaldairy:calving_maternity"))


@login_required
@require_http_methods(['POST'])
def delete_cow_insurance(request):
	cow_insurance_id = request.POST.get('insurance_id')
	cow_insurance = get_object_or_404(CowInsurance, pk=cow_insurance_id)
	cow_insurance.delete()
	return HttpResponseRedirect(reverse("digitaldairy:cow_insurance"))
