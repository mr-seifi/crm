from django.conf import settings
import requests
from . import SEND_KEY, LOOKUP_KEY
from .models import BaseSMS, RegularSMS, ApplianceSMS


class SMSService:

    def __init__(self, model: BaseSMS = RegularSMS):
        self.queryset = model.objects.all()
        self.endpoints = {
            SEND_KEY: 'https://api.kavenegar.com/v1/{api_key}/sms/send.json'.format(api_key=self._api_key),
            LOOKUP_KEY: 'https://api.kavenegar.com/v1/{api_key}/verify/lookup.json'.format(api_key=self._api_key)
        }

    @property
    def _api_key(self) -> str:
        return settings.KAVENEGAR_API_KEY

    def send_by_object(self, sms_obj: BaseSMS):
        key, payload = sms_obj.get_payload()
        endpoint = self.endpoints.get(key)

        response = requests.post(url=endpoint,
                                 data=payload)
        print(response.status_code, response.text)
