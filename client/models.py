from myaccountant.basemodels import BaseModel
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Shop(BaseModel):
    name = models.CharField(max_length=200)
    contact_no = models.CharField(_("Mobile Number"), max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=100, default="", null=True, blank=True)
    address = models.TextField(max_length=1000)
    beat = models.CharField(max_length=200)
    gst = models.CharField(max_length=200, null=True, blank=True, verbose_name="GST Number")
    outstanding_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name}({self.beat})"

