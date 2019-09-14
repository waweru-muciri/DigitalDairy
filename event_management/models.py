from django.db import models

# Create your models here.


class Clients(models.Model):
	id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.CharField(max_length=30, blank=True, default='')
	address = models.CharField(max_length=50, blank=True, default='')
	phone_number = models.CharField(max_length=50, blank=True, default='')

	def __str__(self):
		return '{0} {1}'.format(self.first_name, self.last_name)

	class Meta:
		db_table = 'events_clients'


class Items(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	category = models.CharField(max_length=100)
	description = models.CharField(max_length=100)
	unit_price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return '{0} {1}'.format(self.name, self.quantity)

	class Meta:
		db_table = 'items'


class Quotations(models.Model):
	id = models.AutoField(primary_key=True)
	venue = models.CharField(max_length=100)
	venue_color = models.CharField(max_length=30)
	event_date = models.DateField()
	quote_date = models.DateField()
	client = models.ForeignKey(Clients, on_delete=models.CASCADE)
	total_quotation_amount = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return '{0} {1}'.format(self.client, self.quote_date)

	class Meta:
		db_table = 'quotations'


class Deliveries(models.Model):
	id = models.AutoField(primary_key=True)
	delivery_date = models.DateField()
	quotation = models.ForeignKey(Quotations, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return '{0} {1}'.format(self.quotation, self.delivery_date)

	class Meta:
		db_table = 'deliveries'


class Invoices(models.Model):
	id = models.AutoField(primary_key=True)
	venue = models.CharField(max_length=100)
	venue_color = models.CharField(max_length=100)
	event_date = models.DateField()
	invoice_date = models.DateField()
	delivery = models.ForeignKey(Deliveries, null=True, on_delete=models.SET_NULL)
	total_invoice_amount = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return '{0} {1}'.format(self.delivery, self.invoice_date)

	class Meta:
		db_table = 'invoices'


class Receipts(models.Model):
	id = models.AutoField(primary_key=True)
	receipt_date = models.DateField()
	invoice = models.ForeignKey(Invoices, on_delete=models.CASCADE)
	received_amount = models.DecimalField(max_digits=10, decimal_places=2)
	total = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return '{0} {1}'.format(self.id, self.receipt_date)

	class Meta:
		db_table = 'receipts'


class StandardQuotations(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)

	def __str__(self):
		return '{0}'.format(self.name)

	class Meta:
		db_table = 'standard_quotations'


class QuotationParts(models.Model):
	id = models.AutoField(primary_key=True)
	quotation = models.ForeignKey(Quotations, on_delete=models.SET_NULL, null=True)
	delivery = models.ForeignKey(Deliveries, on_delete=models.SET_NULL, null=True)
	standard_quotation = models.ForeignKey(StandardQuotations, on_delete=models.SET_NULL, null=True)
	item = models.ForeignKey(Items, on_delete=models.CASCADE)
	unit_price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return '{0} {1}'.format(self.item, self.quantity)

	class Meta:
		db_table = 'quotation_parts'
