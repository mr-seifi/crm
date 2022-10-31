from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('tx_hash', 'appliance', 'price', 'created',)
        read_only_fields = ('tx_hash', 'created',)
