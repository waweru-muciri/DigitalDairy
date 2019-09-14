from fcm_django.models import FCMDevice
from apscheduler.schedulers.background import BackgroundScheduler
from digitaldairy.models import Cow, AiRecords, Vaccinations, Deworming
from datetime import date
import dateutil.relativedelta



# NOTE filter the user properly here
def send_push_messages():
	# get the devices to send the messages to
	fcm_device = FCMDevice.objects.all()
	current_date = date.today()
	current_day_dryings_count = AiRecords.objects.filter(drying_date=current_date).count()
	current_day_steamings_count = AiRecords.objects.filter(steaming_date=current_date).count()
	current_day_pregnancy_checks_count = AiRecords.objects.filter(pregnancy_check_date=current_date).count()
	current_day_calvings_count = AiRecords.objects.filter(due_date=current_date).count()
	current_day_dewormings_count = Deworming.objects.filter(next_deworming_date=current_date).count()
	current_day_vaccinations_count = Vaccinations.objects.filter(next_vaccination_date=current_date).count()
	if current_day_calvings_count or current_day_dryings_count or current_day_steamings_count or current_day_pregnancy_checks_count or current_day_dewormings_count or current_day_vaccinations_count:
		response = fcm_device.send_message(click_action="https://digitaldairy.herokuapp.com/digitaldairy/daily_alerts", title= "Breeding & Deworming Updates", body="Daily breeding & deworming updates", icon= "/static/images/icons/digital_dairy128.png")
		print('Sent push message!')
		print('Response from sending push message --> ', response)

def start():
	scheduler = BackgroundScheduler()
	scheduler.add_job(send_push_messages, 'interval', days=1)
	scheduler.start()