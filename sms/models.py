from django.db import models
from abc import ABC, abstractmethod
from typing import Tuple
from . import SEND_KEY, LOOKUP_KEY, TEMPLATES, MESSAGE, RECEPTOR, TOKEN, TOKEN2, TOKEN3, TEMPLATE


class BaseSMS(models.Model):
    is_sent = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def get_payload(self) -> Tuple[str, dict]:
        ...

    def get_receptor(self) -> str:
        ...

    class Meta:
        verbose_name_plural = 'Base SMSes'


class RegularSMS(BaseSMS):
    customer = models.ForeignKey(to='management.Customer', on_delete=models.CASCADE)
    text = models.TextField()

    def get_payload(self) -> Tuple[str, dict]:
        return SEND_KEY, {MESSAGE: self.text,
                          RECEPTOR: self.get_receptor()}

    def get_receptor(self) -> str:
        return self.customer.phone

    class Meta:
        verbose_name_plural = 'Regular SMSes'


class ApplianceSMS(BaseSMS):
    appliance = models.ForeignKey(to='management.Appliance', on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        state_delivered = self.StateDelivered(parent=self)
        state_ready = self.StateReady(parent=self, next=state_delivered)
        state_received = self.StateReceived(parent=self, next=state_ready)

        self._handler = state_received

    def get_payload(self) -> Tuple[str, dict]:
        payload, _handler = self._handler.handle()

        if not self.is_sent:
            return LOOKUP_KEY, payload

        if not _handler:
            return '', {}

        self._handler = _handler
        self.is_sent = False
        self.save()

        text, _ = self._handler.handle()
        return LOOKUP_KEY, payload

    def get_receptor(self) -> str:
        return self.appliance.customer.phone

    class Meta:
        verbose_name_plural = 'Appliance SMSes'

    # Chain-of-responsibility
    class StateHandler(ABC):

        def __init__(self, next=None, parent=None):
            self.next = next
            self.parent = parent

        def handle(self):
            return self._handle(), self.next

        @abstractmethod
        def _handle(self):
            ...

    class StateReceived(StateHandler):

        def _handle(self):
            return {
                RECEPTOR: self.parent.get_receptor(),
                TEMPLATE: TEMPLATES['isReceived'],
                TOKEN: self.parent.appliance.id,
                TOKEN2: '1400' or self.parent.appliance.created,
            }

    class StateReady(StateHandler):

        def _handle(self):
            return {
                RECEPTOR: self.parent.get_receptor(),
                TEMPLATE: TEMPLATES['isReady'],
                TOKEN: self.parent.appliance.price or '',
            }

    class StateDelivered(StateHandler):

        def _handle(self):
            return {
                RECEPTOR: self.parent.get_receptor(),
                TEMPLATE: TEMPLATES['isDelivered'],
                TOKEN: self.parent.appliance.id,
                TOKEN2: self.parent.appliance.created,  # TODO: now - persian
            }
