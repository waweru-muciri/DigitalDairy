from rest_framework import viewsets, permissions
from .serializers import *
from .models import Items


#Item viewset
class ItemViewSet(viewsets.ModelViewSet):
	queryset = Items.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = ItemSerializer


#Deliveries viewset
class DeliveriesViewSet(viewsets.ModelViewSet):
	queryset = Deliveries.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = DeliveriesSerializer


#Clients viewset
class ClientsViewSet(viewsets.ModelViewSet):
	queryset = Clients.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = ClientsSerializer


#Invoices viewset
class InvoicesViewSet(viewsets.ModelViewSet):
	queryset = Invoices.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = InvoicesSerializer


#Quotations viewset
class QuotationsViewSet(viewsets.ModelViewSet):
	queryset = Quotations.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = QuotationsSerializer


#StandardQuotations viewset
class StandardQuotationsViewSet(viewsets.ModelViewSet):
	queryset = StandardQuotations.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = StandardQuotationsSerializer


#QuotationParts viewset
class QuotationPartsViewSet(viewsets.ModelViewSet):
	queryset = QuotationParts.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = QuotationPartsSerializer


