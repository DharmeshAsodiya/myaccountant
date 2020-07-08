from django.contrib import admin
from myaccountant.baseadmin import BaseAdmin
from .models import Order, Invoice, OrderItem
from django.utils.html import format_html


@admin.register(OrderItem)
class OrderItemAdmin(BaseAdmin):

    list_display = ('id', "product", "quantity")
    list_filter = ('created_on',)
    search_fields = ('product__name',)

    actions = ["export_as_csv"]
    csv_headers = ['Product', 'Quantity', 'Rate', 'Billing Date', 'Order Id', 'Shop']
    csv_columns = ['product__name', 'quantity', 'mrp', 'created_on__date', 'order__id',
                   'order__customer__name']
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(BaseAdmin):

    list_display = ('id', "customer")
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Invoice)
class InvoiceAdmin(BaseAdmin):

    list_display = ('order', "sub_total", "outstanding_amount", "invoice_link")

    def invoice_link(self, obj):
        if not obj.invoice_details:
            return None
        return format_html(f'<a href="/admin/order/display-invoice/?id={obj.id}" target="_blank">Invoice Statement</a>')

    invoice_link.short_description = "Invoice"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
