from .models import Exchange
from rest_framework import serializers

class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'
        read_only_fields = ('date',)