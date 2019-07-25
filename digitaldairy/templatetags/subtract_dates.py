from django import template
import datetime
register = template.Library()


@register.filter 
def minus_dates(value, arg):
	print(value)
	value = datetime.datetime.strptime(value, '%m/%d/%Y').date()
	return (value - arg).days


# register.filter(minus_dates)