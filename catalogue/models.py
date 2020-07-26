from myaccountant.basemodels import BaseModel
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Product(BaseModel):
    name = models.CharField(max_length=1000)
    hsn_code = models.CharField(max_length=200)
    cost_price = models.DecimalField(max_digits=15, decimal_places=2)
    mrp = models.DecimalField(max_digits=15, decimal_places=2)
    tax_value = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"({self.hsn_code}) {self.name}"


class Stock(BaseModel):
    product = models.ForeignKey(Product, on_delete=True, unique=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"Product:{self.product} Quantity:{self.quantity}"


class Supplier(BaseModel):
    name = models.CharField(max_length=200)
    contact_no = models.CharField(_("Mobile Number"), max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=100, default="", null=True, blank=True)
    address = models.TextField(max_length=1000)
    gst = models.CharField(max_length=200, null=True, blank=True, verbose_name="GST Number")
    outstanding_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name}"


class StockInwardDetails(BaseModel):

    STOCK_ADD = 0
    SUPPLIER_RETURN = 1
    SHOP_RETURN = 2

    TRANSACTION_TYPE = ((STOCK_ADD, "Add Stock"),
                        (SUPPLIER_RETURN, "Return to Supplier"),
                        (SHOP_RETURN, "Return from Shop")
                        )

    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=0)
    type = models.PositiveSmallIntegerField(choices=TRANSACTION_TYPE, default=0)
    po_number = models.CharField(max_length=100, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    mrp = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    stock_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    supplier = models.ForeignKey(Supplier, null=True, on_delete=models.DO_NOTHING)
