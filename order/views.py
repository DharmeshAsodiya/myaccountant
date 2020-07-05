import json
from decimal import Decimal
from myaccountant.baseviews import BaseAdminViews
from django.views import View
from client.models import Shop
from .services.ordercreator import OrderCreator
from .models import Invoice


class OrderCreateView(BaseAdminViews):

    template_name = "order/ordercreate.html"

    def get_context_data(self, **kwargs):
        shops = Shop.objects.all().values("id", "name", "beat")
        context_data = {"shops": shops}
        return context_data

    def post(self, request):
        shop_id = request.POST.get("shop_id")
        product_list = request.POST.getlist("product_id")
        quantity_list = request.POST.getlist("quantity")
        price_list = request.POST.getlist("mrp")
        request_type = request.POST.get("submit_type")
        order_service = OrderCreator(shop_id, product_list, quantity_list, price_list)
        if request_type == "create-order":
            order_service.create_order()
        context_data = order_service.get_invoice_data()
        self.template_name = "order/invoice.html"
        return self.render_to_response(context_data)


class InvoiceView(BaseAdminViews):

    def get(self, request):
        invoice = Invoice.objects.get(id=request.GET.get('id'))
        self.template_name = "order/invoice.html"
        return self.render_to_response(json.loads(invoice.invoice_details))
