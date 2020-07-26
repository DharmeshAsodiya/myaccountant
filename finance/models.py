from myaccountant.basemodels import BaseModel
from django.db import models


class PaymentLedger(BaseModel):
    SUPPLIER = 0
    SHOP = 1

    CLIENT_TYPE = ((SUPPLIER, "Supplier"),
                   (SHOP, "Shop"))
    CASH = 0
    CHEQUE = 1
    NEFT = 2
    PAYMENT_MODE = ((CASH, "Cash"),
                    (CHEQUE, "Cheque"),
                    (NEFT, "NEFT"))

    client_id = models.IntegerField()
    client_type = models.PositiveSmallIntegerField(choices=CLIENT_TYPE)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2)
    paid_at = models.DateTimeField(auto_now=True)
    payment_mode = models.PositiveSmallIntegerField(default=CASH, choices=PAYMENT_MODE)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
