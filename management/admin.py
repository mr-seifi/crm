from django.contrib import admin, messages
from .models import Customer, Appliance
from django.db.models import Count, Sum
from django.utils.html import format_html, urlencode
from django.urls import reverse
from payment.admin import TransactionInline
from . import LOYAL_CUSTOMER_BOUNDARY


class CustomerStatusFilter(admin.SimpleListFilter):
    title = 'customer_status'
    parameter_name = 'customer_status'
    _NORMAL = f'<{LOYAL_CUSTOMER_BOUNDARY}'
    _LOYAL = f'>{LOYAL_CUSTOMER_BOUNDARY - 1}'

    def lookups(self, request, model_admin):
        return [
            (self._NORMAL, 'Normal'),
            (self._LOYAL, 'Loyal')
        ]

    def queryset(self, request, queryset):
        queryset = queryset.annotate(
            appliance_count=Count('appliance')
        )
        if self.value() == self._NORMAL:
            return queryset.filter(
                appliance_count__lt=LOYAL_CUSTOMER_BOUNDARY + 1
            )
        elif self.value() == self._LOYAL:
            return queryset.filter(
                appliance_count__gte=LOYAL_CUSTOMER_BOUNDARY + 1
            )
        return queryset


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    actions = ('calculate_earned',)
    list_display = ('name', 'phone', 'customer_loyalty',)
    list_per_page = 100
    list_filter = (CustomerStatusFilter,)
    ordering = ('name', 'phone',)
    search_fields = ('name', 'phone',)

    def get_queryset(self, request):
        queryset = super(CustomerAdmin, self).get_queryset(request)
        return queryset.annotate(
            appliance_count=Count('appliance'),
            appliance_earned=Sum('appliance__transaction__price')
        )

    @staticmethod
    @admin.display(ordering='appliance_count')
    def customer_loyalty(customer):
        if customer.appliance_count > LOYAL_CUSTOMER_BOUNDARY:
            customer_status = 'Loyal'
        else:
            customer_status = 'Normal'

        url = (
                reverse('admin:management_appliance_changelist')
                + '?'
                + urlencode({'customer__id': customer.id})
        )
        return format_html('<a href="{}">{}</a>', url, customer_status)

    @admin.action(description='Calculate earned')
    def calculate_earned(self, request, queryset):
        price_sum = sum(filter(lambda x: x is not None, queryset.values_list("appliance_earned", flat=True)))
        self.message_user(
            request,
            f'{price_sum or 0:,} Toman earned from these users!',
            messages.SUCCESS
        )


@admin.register(Appliance)
class ApplianceAdmin(admin.ModelAdmin):
    actions = ('calculate_total_value',)
    autocomplete_fields = ('customer',)
    inlines = (TransactionInline,)
    list_display = ('name', 'brand', 'customer', 'state', 'cs_price', 'created', 'updated',)
    list_per_page = 50
    list_filter = ('brand', 'state', 'updated',)
    ordering = ('-updated', '-created',)
    search_fields = ('name', 'brand', 'customer__name', 'price',)

    @admin.action(description='Calculate total value')
    def calculate_total_value(self, request, queryset):
        price_sum = queryset.aggregate(earned=Sum('price'))['earned']
        self.message_user(
            request,
            f'{price_sum or 0:,} Toman earned from these users!',
            messages.SUCCESS
        )
