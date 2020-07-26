from django.contrib import admin
from myaccountant.baseadmin import BaseAdmin
from .models import PaymentLedger
from client.models import Shop
from catalogue.models import Supplier
from django.utils.html import format_html
from django.http.response import HttpResponseRedirect


@admin.register(PaymentLedger)
class PaymentLedgerAdmin(BaseAdmin):
    list_display = ('id', "client_name", "client_type", "paid_amount", "payment_mode", "paid_at" )
    list_filter = ('created_on',)

    # actions = ["export_as_csv"]
    # csv_headers = ['Product', 'Quantity', 'Rate', 'Billing Date', 'Order Id', 'Shop']
    # csv_columns = ['product__name', 'quantity', 'mrp', 'created_on__date', 'order__id',
    #                'order__customer__name']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def client_name(self, obj):
        if obj.client_type == self.model.SHOP:
            query_model = Shop
        else:
            query_model = Supplier
        client = query_model.objects.get(id=obj.client_id)
        return f"{client.name}"

    def lookup_allowed(self, lookup, value):
        """Override the default changelist view
        IF GET parameter is null redirect to search page
        """
        return True

    def changelist_view(self, request, extra_context=None):

        get_parms = request.GET.keys()
        if 'e' in get_parms:
            get_parms.remove('e')
        if not get_parms:
            return HttpResponseRedirect('/admin/finance/payment-ledger/search')
        else:
            return super(PaymentLedgerAdmin, self)\
                .changelist_view(request, extra_context=extra_context)
