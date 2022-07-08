from django.forms import Form, ChoiceField, DecimalField, CharField
from django.utils.translation import gettext_lazy as _

class PaymentForm(Form):
    currency = ChoiceField(
        choices=(("UAH", "UAH"), ("USD", "USD"), ("EUR", "EUR")),
        label=_("Валюта платежу")
    )
    amount = DecimalField(min_value=0.01, decimal_places=2, label=_("Сума пожертви"))
    project = CharField(required=True)