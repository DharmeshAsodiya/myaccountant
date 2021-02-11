import json
from decimal import Decimal
from myaccountant.baseviews import BaseAdminViews
from django.views import View
from django.contrib import messages
from client.models import Shop
from .services.ordercreator import OrderCreator
from .models import Order
from django.utils.safestring import mark_safe


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
            try:
                order_id = order_service.create_order()
            except Exception as e:
                messages.error(request,
                                 mark_safe("Order creation failed !!! %s" % e))
                return self.render_to_response(self.get_context_data())

            messages.success(request,
                             mark_safe("Order created successfully, "
                                       "<a href=/admin/order/display-invoice/?id=%s>"
                                       "Download invoice</a>" % order_id))
            return self.render_to_response(self.get_context_data())

        # preview invoice response
        invoice_data = order_service.get_invoice_data()
        self.template_name = "order/invoice.html"
        return self.render_to_response(invoice_data)


class InvoiceView(BaseAdminViews):

    template_name = "order/invoice.html"

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=request.GET.get('id'))
        return self.render_to_response(json.loads(order.invoice_details))
