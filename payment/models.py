from django.db import models
from uuid import uuid4


class Transaction(models.Model):
    appliance = models.ForeignKey(to='management.Appliance', on_delete=models.PROTECT)
    tx_hash = models.UUIDField(primary_key=True, default=uuid4)
    price = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def _calculate_price(self) -> int:
        paid = self.appliance.transaction_set.aggregate(paid=models.Sum('price'))['paid'] or 0
        return self.appliance.price - paid

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self._calculate_price()

        return super(Transaction, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)
