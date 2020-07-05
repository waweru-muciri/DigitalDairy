from rest_framework import serializers
from digitaldairy.models import *


# Cow serializer
class CowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cow
        fields = '__all__'


class SemenRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemenRecords
        fields = '__all__'


class CowBodyTraitsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CowBodyTraits
        fields = '__all__'


class MilkTargetsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MilkTargets
        fields = '__all__'


class ClientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Clients
        fields = '__all__'


class ConsumersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consumers
        fields = '__all__'


class MilkSalesSerializer(serializers.ModelSerializer):

    class Meta:
        model = MilkSales
        fields = '__all__'


class MilkConsumptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MilkConsumptions
        fields = '__all__'


class MilkProductionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MilkProductions
        fields = '__all__'


class WeightRecordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeightRecords
        fields = '__all__'


class CowSalesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CowSales
        fields = '__all__'


class TreatmentRecordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TreatmentRecords
        fields = '__all__'


class DewormingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deworming
        fields = '__all__'


class VaccinationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vaccinations
        fields = '__all__'


class DiseasesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Diseases
        fields = '__all__'


class DeathsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deaths
        fields = '__all__'


class MilkSalesPaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MilkSalesPayments
        fields = '__all__'


class AiRecordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AiRecords
        fields = '__all__'


class CalvingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calvings
        fields = '__all__'


class AbortionMiscarriagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AbortionMiscarriages
        fields = '__all__'


class EmployeesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employees
        fields = '__all__'


class SalaryAdvancesSerializer(serializers.ModelSerializer):

    class Meta:
        model = SalaryAdvances
        fields = '__all__'


class EmployeeSalariesSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeSalaries
        fields = '__all__'


class CalfFeedingSerializer(serializers.ModelSerializer):

    class Meta:
        model = CalfFeeding
        fields = '__all__'


class FeedItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedItems
        fields = '__all__'


class DailyFeedingSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyFeeding
        fields = '__all__'


class CowInsuranceSerializer(serializers.ModelSerializer):

    class Meta:
        model = CowInsurance
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = '__all__'
