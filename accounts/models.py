from django.db import models
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
	instance.userprofile.save()


post_save.connect(create_profile, sender=User)
post_save.connect(save_profile, sender=User)

