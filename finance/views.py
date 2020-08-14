from decimal import Decimal
from myaccountant.baseviews import BaseAdminViews
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from .models import PaymentLedger
from .forms import PaymentDetailForm, PaymentLedgerSearchForm
from catalogue.models import Supplier
from client.models import Shop
from order.models import Order


class SupplierPaymentView(BaseAdminViews):

    template_name = "finance/pay_supplier.html"

    def get_context_data(self, **kwargs):
        return {"form": PaymentDetailForm()}

    def post(self, request):
        supplier_id = request.POST.get("client_id")
        amount = request.POST.get("paid_amount")
        paid_at = request.POST.get("payment_date")
        mode = request.POST.get("payment_mode")
        if not supplier_id:
            messages.error(request, "Suppler not found in system with ID: %s" % supplier_id)
            return self.render_to_response(self.get_context_data())

        supplier = Supplier.objects.get(id=supplier_id)
        PaymentLedger.objects.create(client_id=supplier_id, client_type=PaymentLedger.SUPPLIER,
                                     paid_amount=amount,
                                     # paid_at=paid_at,
                                     payment_mode=mode)
        # increasing supplier balance
        supplier.outstanding_balance -= Decimal(amount)
        supplier.save()
        messages.success(request, "Payment detail Updated, Final outstanding Balance for %s is %s" % (supplier.name, supplier.outstanding_balance))
        return self.render_to_response(self.get_context_data())


class ShopPaymentView(BaseAdminViews):

    template_name = "finance/shop_payment.html"

    def get_context_data(self, **kwargs):
        return {"form": PaymentDetailForm()}

    def post(self, request):
        supplier_id = request.POST.get("client_id")
        amount = request.POST.get("paid_amount")
        paid_at = request.POST.get("payment_date")
        mode = request.POST.get("payment_mode")
        if not supplier_id:
            messages.error(request, "Suppler not found in system with ID: %s" % supplier_id)
            return self.render_to_response(self.get_context_data())
        amount = Decimal(amount)
        shop = Shop.objects.get(id=supplier_id)
        PaymentLedger.objects.create(client_id=shop.id, client_type=PaymentLedger.SHOP,
                                     paid_amount=amount,
                                     # paid_at=paid_at,
                                     payment_mode=mode)
        # decreasing shop outstanding balance
        shop.outstanding_balance -= amount
        orders = Order.objects.filter(customer=shop, outstanding_amount__gt=Decimal(0))\
            .order_by('id')
        import ipdb;ipdb.set_trace()
        for o in orders:
            if amount <= 0:
                break
            if amount >= o.outstanding_amount:
                amount -= o.outstanding_amount
                o.outstanding_amount = Decimal(0)
            else:
                o.outstanding_amount -= amount
                amount = Decimal(0)
            o.save()

        shop.save()
        messages.success(request, "Payment detail Updated, Final outstanding Balance for %s is %s"
                         % (shop.name, shop.outstanding_balance))
        return self.render_to_response(self.get_context_data())


class PaymentLedgerSearchView(BaseAdminViews):

    template_name = "common/search.html"

    def get_context_data(self, **kwargs):
        return {"form": PaymentLedgerSearchForm(),
                "view_name": "Payment Ledger",
                "app": "finance"}

    def post(self, request):
        return HttpResponseRedirect("/admin/finance/paymentledger/?client_type=%s" %
                                    request.POST.get("client_type"))