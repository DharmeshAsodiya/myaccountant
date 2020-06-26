from django.contrib import admin
from myaccountant.baseadmin import BaseAdmin
from .models import Order, Invoice

# Register your models here.
@admin.register(Order)
class OrderAdmin(BaseAdmin):

    list_display = ('id', "customer")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Invoice)
class InvoiceAdmin(BaseAdmin):

    list_display = ('order', "sub_total","outstanding_amount")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
