from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        if 'customer_pk' in self.kwargs:
            return Transaction.objects.filter(appliance__customer_id=self.kwargs['customer_pk'])
        return Transaction.objects.all()

    def get_serializer_context(self):
        return {
            'customer_id': self.kwargs.get('customer_pk', None),
            **super(TransactionViewSet, self).get_serializer_context()
        }
