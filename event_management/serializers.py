from rest_framework import serializers
from .models import *
from dateutil import parser


# item serializer
class ItemSerializer(serializers.ModelSerializer):

	def validate_amount(self, value):
		if not value.isdigit():
			raise serializers.ValidationError('Value must be a digit.')
		return value

	class Meta:
		model = Items
		fields = '__all__'
		# extra_kwargs = {
		# 	'password': {'write_only': True}
		# }


class DeliveriesSerializer(serializers.ModelSerializer):

	def to_internal_value(self, data):
		data['delivery_date']  = parser.parse(data['delivery_date'])	
		return super().to_internal_value(data)

	class Meta:
		model = Deliveries
		fields = '__all__'


class ClientsSerializer(serializers.ModelSerializer):

	class Meta:
		model = Clients
		fields = '__all__'


class InvoicesSerializer(serializers.ModelSerializer):

	def to_internal_value(self, data):
		data['event_date']  = parser.parse(data['event_date'])
		data['invoice_date']  = parser.parse(data['invoice_date'])
		return super().to_internal_value(data)

	class Meta:
		model = Invoices
		fields = '__all__'


class QuotationsSerializer(serializers.ModelSerializer):

	def to_internal_value(self, data):
		data['event_date']  = parser.parse(data['event_date'])
		data['quote_date']  = parser.parse(data['quote_date'])
		return super().to_internal_value(data)

	class Meta:
		model = Quotations
		fields = '__all__'


class StandardQuotationsSerializer(serializers.ModelSerializer):

	class Meta:
		model = StandardQuotations
		fields = '__all__'


class QuotationPartsSerializer(serializers.ModelSerializer):

	class Meta:
		model = QuotationParts
		fields = '__all__'



