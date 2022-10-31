from django.db.models import Sum, Count
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer, Appliance
from .serializers import CustomerSerializer, ApplianceSerializer
from .filters import CustomerFilterSet, ApplianceFilterSet


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.annotate(
        appliance_count=Count('appliance'),
        earned=Sum('appliance__transaction__price'),
    )
    serializer_class = CustomerSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filterset_class = CustomerFilterSet
    search_fields = ('name', 'phone',)
    ordering_fields = ('name', 'phone', 'created',)


class ApplianceViewSet(ModelViewSet):
    queryset = Appliance.objects.all()
    serializer_class = ApplianceSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filterset_class = ApplianceFilterSet
    search_fields = ('name', 'brand', 'description', 'customer__name',)
    ordering_fields = ('name', 'brand', 'customer__name', 'price', 'updated',)
