from django import forms
from .models import Supplier


class SupplierAddForms(forms.ModelForm):

    class Meta:
        model = Supplier
        exclude = ('outstanding_balance', 'created_by', 'updated_by', 'created_on', 'updated_on')
