from myaccountant.baseadmin import BaseAdmin
from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    search_fields = ('hsn_code', 'name')
    list_display = ('id', 'name', 'hsn_code', 'cost_price', 'mrp')


@admin.register(Stock)
class StockAdmin(BaseAdmin):
    search_fields = ('product',)
    list_display = ('id', 'product', 'quantity', 'created_by', 'updated_by', 'created_on', 'updated_on')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


@admin.register(StockInwardDetails)
class StockInwardAdmin(BaseAdmin):
    search_fields = ('product',)
    list_display = ('id', 'product', 'quantity', 'cost_price', 'created_on', 'updated_on')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

