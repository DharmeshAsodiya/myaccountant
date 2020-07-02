from myaccountant.basemodels import BaseModel
from django.db import models


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


class StockInwardDetails(BaseModel):
    product = models.ForeignKey(Product, on_delete=True)
    quantity = models.IntegerField(default=0)
    po_number = models.CharField(max_length=100, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    mrp = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    stock_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
