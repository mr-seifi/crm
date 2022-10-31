from django.contrib import admin
from .models import RegularSMS, ApplianceSMS


@admin.register(RegularSMS)
class RegularSMSAdmin(admin.ModelAdmin):
    actions = ('send_sms',)
    autocomplete_fields = ('customer',)
    list_display = ('customer', 'customer_phone', 'text', 'is_sent', 'created',)
    list_filter = ('is_sent', 'created',)
    list_per_page = 10
    ordering = ('-created',)

    @staticmethod
    def customer_phone(regular_sms):
        return regular_sms.customer.phone

    @admin.action(description='Send SMS')
    def send_sms(self):
        ...


@admin.register(ApplianceSMS)
class ApplianceSMSAdmin(admin.ModelAdmin):
    actions = ('send_sms',)
    autocomplete_fields = ('appliance',)
    list_display = ('appliance', 'customer', 'customer_phone', 'is_sent', 'created',)
    list_filter = ('is_sent', 'created',)
    list_per_page = 10
    ordering = ('-created',)
    search_fields = ('text', 'appliance__id', 'appliance__name', 'appliance__customer__phone',)

    @staticmethod
    def customer(appliance_sms):
        return appliance_sms.appliance.customer

    @staticmethod
    def customer_phone(appliance_sms):
        return appliance_sms.appliance.customer.phone

    @admin.action(description='Send SMS')
    def send_sms(self):
        ...
