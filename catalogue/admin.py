from myaccountant.baseadmin import BaseAdmin
from django.contrib import admin
from .forms import SupplierAddForms
from .models import *


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    search_fields = ('hsn_code', 'name')
    list_display = ('id', 'name', 'hsn_code', 'cost_price', 'mrp')


@admin.register(Supplier)
class SupplierAdmin(BaseAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name', 'contact_no', 'gst', 'outstanding_balance')
    form = SupplierAddForms


@admin.register(Stock)
class StockAdmin(BaseAdmin):
    search_fields = ('product__name',)
    list_display = ('id', 'product', 'quantity', 'created_by', 'updated_by', 'created_on',
                    'updated_on')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


@admin.register(StockInwardDetails)
class StockInwardAdmin(BaseAdmin):
    search_fields = ('product__name', 'po_number')
    list_filter = ('supplier', 'type', 'created_on')
    list_display = ('product', 'supplier', 'po_number', 'type', 'quantity', 'cost_price', 'mrp', 'stock_value',
                    'created_on', 'updated_on')

    actions = ["export_as_csv"]
    csv_headers = ['Product', 'Quantity', 'Cost Price', 'MRP', 'Stock Value', "Purchase Date"]
    csv_columns = ['product__name', 'quantity', 'cost_price', 'mrp', 'stock_value',
                   'created_on__date']
    csv_file_name = "stock_inward_report"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

