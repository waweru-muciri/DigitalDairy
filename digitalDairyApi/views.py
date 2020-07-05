from rest_framework import viewsets, permissions
from .serializers import *
from digitaldairy.models import *


class CowsViewSet(viewsets.ModelViewSet):
	queryset = Cow.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = CowSerializer



class SemenRecordsViewSet(viewsets.ModelViewSet):
	queryset = SemenRecords.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = SemenRecordsSerializer


class DailyFeedingViewSet(viewsets.ModelViewSet):
	queryset = DailyFeeding.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = DailyFeedingSerializer


class CowBodyTraitsViewSet(viewsets.ModelViewSet):
	queryset = CowBodyTraits.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = CowBodyTraitsSerializer


class MilkTargetsViewSet(viewsets.ModelViewSet):
	queryset = MilkTargets.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = MilkTargetsSerializer


class ClientsViewSet(viewsets.ModelViewSet):
	queryset = Clients.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = ClientsSerializer


class ConsumersViewSet(viewsets.ModelViewSet):
	queryset = Consumers.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = ConsumersSerializer


class MilkSalesViewSet(viewsets.ModelViewSet):
	queryset = MilkSales.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = MilkSalesSerializer


class MilkConsumptionsViewSet(viewsets.ModelViewSet):
	queryset = MilkConsumptions.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = MilkConsumptionsSerializer


class MilkProductionsViewSet(viewsets.ModelViewSet):
	queryset = MilkProductions.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = MilkProductionsSerializer


class WeightRecordsViewSet(viewsets.ModelViewSet):
	queryset = WeightRecords.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = WeightRecordsSerializer


class CowSalesViewSet(viewsets.ModelViewSet):
	queryset = CowSales.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = CowSalesSerializer


class TreatmentRecordsViewSet(viewsets.ModelViewSet):
	queryset = TreatmentRecords.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = TreatmentRecordsSerializer


class DewormingViewSet(viewsets.ModelViewSet):
	queryset = Deworming.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = DewormingSerializer


class VaccinationsViewSet(viewsets.ModelViewSet):
	queryset = Vaccinations.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = VaccinationsSerializer


class DiseasesViewSet(viewsets.ModelViewSet):
	queryset = Diseases.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = DiseasesSerializer


class DeathsViewSet(viewsets.ModelViewSet):
	queryset = Deaths.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = DeathsSerializer


class MilkSalesPaymentsViewSet(viewsets.ModelViewSet):
	queryset = MilkSalesPayments.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = MilkSalesPaymentsSerializer


class AiRecordsViewSet(viewsets.ModelViewSet):
	queryset = AiRecords.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = AiRecordsSerializer


class CalvingsViewSet(viewsets.ModelViewSet):
	queryset = Calvings.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = CalvingsSerializer


class AbortionMiscarriagesViewSet(viewsets.ModelViewSet):
	queryset = AbortionMiscarriages.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = AbortionMiscarriagesSerializer


class EmployeesViewSet(viewsets.ModelViewSet):
	queryset = Employees.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = EmployeesSerializer


class SalaryAdvancesViewSet(viewsets.ModelViewSet):
	queryset = SalaryAdvances.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = SalaryAdvancesSerializer


class EmployeeSalariesViewSet(viewsets.ModelViewSet):
	queryset = EmployeeSalaries.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = EmployeeSalariesSerializer


class CalfFeedingViewSet(viewsets.ModelViewSet):
	queryset = CalfFeeding.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = CalfFeedingSerializer


class FeedItemsViewSet(viewsets.ModelViewSet):
	queryset = FeedItems.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = FeedItemsSerializer


class CowInsuranceViewSet(viewsets.ModelViewSet):
	queryset = CowInsurance.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = CowInsuranceSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
	queryset = Expense.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = ExpenseSerializer


class IncomeViewSet(viewsets.ModelViewSet):
	queryset = Income.objects.all()
	permission_classes = [
		permissions.AllowAny
	]
	serializer_class = IncomeSerializer


