from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import CustomerViewSet, ApplianceViewSet
from payment.views import TransactionViewSet


router = DefaultRouter()
router.register('customers', CustomerViewSet)
router.register('appliances', ApplianceViewSet)

customers_router = NestedDefaultRouter(router, 'customers', lookup='customer')
customers_router.register('transactions', TransactionViewSet, basename='customer-transactions')

urlpatterns = router.urls + customers_router.urls
