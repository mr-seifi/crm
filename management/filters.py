from django_filters import FilterSet, CharFilter
from .models import Customer, Appliance
from . import LOYAL_CUSTOMER_BOUNDARY


class CustomerFilterSet(FilterSet):
    status = CharFilter(method='get_status')

    @staticmethod
    def get_status(queryset, _, value):
        if value in ('Loyal', 'loyal'):
            return queryset.filter(appliance_count__gt=LOYAL_CUSTOMER_BOUNDARY)
        elif value in ('Normal', 'normal'):
            return queryset.filter(appliance_count__lte=LOYAL_CUSTOMER_BOUNDARY)
        return queryset

    class Meta:
        model = Customer
        fields = ('status',)


class ApplianceFilterSet(FilterSet):

    class Meta:
        model = Appliance
        fields = {
            'brand': ('exact', 'in',),
            'state': ('exact', 'in',),
        }
