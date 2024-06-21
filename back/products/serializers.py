from .models import FinancialCompany, TimeDeposit, TimeDepositOption, Saving, SavingOption
from rest_framework import serializers

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialCompany
        fields = '__all__'

class TimeDeopositSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeDeposit
        fields = '__all__'

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeDepositOption
        fields = '__all__'
        read_only_fields = ('deposit',)


class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saving
        fields = '__all__'

class SavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = '__all__'
        read_only_fields = ('saving',)