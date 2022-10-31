from django.contrib import admin
from .models import Transaction


class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('tx_hash',)
    list_display = ('tx_hash', 'appliance', 'price', 'customer', 'created',)
    list_select_related = ('appliance', 'appliance__customer',)
    list_filter = ('created',)
    list_per_page = 50
    ordering = ('-created',)
    search_fields = ('tx_hash', 'appliance__name', 'appliance__customer__name__istartswith')

    @staticmethod
    def price(transaction):
        return transaction.appliance.cs_price

    @staticmethod
    def customer(transaction):
        return transaction.appliance.customer
