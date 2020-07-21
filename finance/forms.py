from django import forms
from .models import PaymentLedger


class PaymentDetailForm(forms.Form):

    client = forms.HiddenInput()
    client_name = forms.CharField()
    paid_amount = forms.DecimalField()
    payment_mode = forms.ChoiceField(choices=PaymentLedger.PAYMENT_MODE)
    payment_date = forms.DateTimeField(widget=forms.SelectDateWidget)
    transaction_id = forms.CharField(required=False)
    settle_account = forms.BooleanField(widget=forms.CheckboxInput, required=False)


class PaymentLedgerSearchForm(forms.Form):

    client_type = forms.ChoiceField(choices=PaymentLedger.CLIENT_TYPE)

