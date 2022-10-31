from django.db import models
from django.core.validators import MinValueValidator


class Customer(models.Model):
    name = models.CharField(db_index=True, max_length=128)
    phone = models.CharField(db_index=True, unique=True, max_length=16)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('name', 'phone')


class Appliance(models.Model):  # TODO: Chain of responsibility on states...
    NOT_READY = 'NR'
    READY = 'R'
    PAID = 'P'

    STATE_CHOICES = [
        (NOT_READY, 'NOT READY'),
        (READY, 'READY'),
        (PAID, 'PAID')
    ]
    name = models.CharField(max_length=128)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    brand = models.CharField(null=True, max_length=128)
    description = models.TextField(null=True, blank=True)
    state = models.CharField(choices=STATE_CHOICES, default=NOT_READY, max_length=8)
    price = models.IntegerField(null=True, validators=[MinValueValidator(0)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def cs_price(self) -> str:
        return f'{self.price:,}'

    def __str__(self) -> str:
        return f'{self.name} {self.brand}'
