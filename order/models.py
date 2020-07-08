from myaccountant.basemodels import BaseModel
from django.contrib.postgres.fields import JSONField
from client.models import Shop
from catalogue.models import Product
from django.db import models


class Order(BaseModel):
    order_no = models.CharField(max_length=100)
    customer = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET(0))
    quantity = models.IntegerField(default=0)
    mrp = models.DecimalField(max_digits=15, decimal_places=2)


class Invoice(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sub_total = models.DecimalField(max_digits=15, decimal_places=2)
    outstanding_amount = models.DecimalField(max_digits=15, decimal_places=2)
    invoice_details = JSONField(null=True)


class CreditNote(BaseModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2)
    paid_at = models.DateTimeField(auto_now=True)
    payment_mode = models.CharField(max_length=20, default="Cash")
