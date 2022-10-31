from rest_framework import serializers
from .models import Customer, Appliance
from . import LOYAL_CUSTOMER_BOUNDARY


class CustomerSerializer(serializers.ModelSerializer):
    earned = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ('id', 'name', 'phone', 'earned', 'status', 'created',)
        read_only_fields = ('earned', 'status', 'created',)

    @staticmethod
    def get_earned(obj):
        return f'{obj.earned or 0:,}'

    @staticmethod
    def get_status(obj):
        return f'Loyal' if obj.appliance_count > LOYAL_CUSTOMER_BOUNDARY else 'Normal'


class ApplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appliance
        fields = ('id', 'name', 'brand', 'customer', 'description', 'state', 'price', 'created', 'updated',)
        read_only_fields = ('created', 'updated',)
