import inflect

from decimal import Decimal
from myaccountant.baseviews import BaseAdminViews
from django.contrib import messages
from django.http.response import JsonResponse, HttpResponseRedirect
from .models import Order, OrderItem, Invoice
from catalogue.models import Product, Stock
from client.models import Shop


class OrderCreateView(BaseAdminViews):

    template_name = "order/ordercreate.html"

    def get_context_data(self, **kwargs):
        shops = Shop.objects.all().values("id", "name", "beat")
        context_data = {"shops": shops}
        return context_data

    def post(self, request):
        print(request.POST)
        order_id = self.create_order(request)
        inf = inflect.engine()
        shop_id = request.POST.get("shop_id")
        product_list = request.POST.getlist("product_id")
        quantity_list = request.POST.getlist("quantity")
        # cost_price = request.POST.get("cp")
        price_list = request.POST.getlist("mrp")
        item_list = []
        sub_total = 0

        for idx in range(len(product_list)):
            p_id = product_list[idx]
            product = Product.objects.get(id=p_id)
            quantity = float(quantity_list[idx])
            # cost_price = request.POST.get("cp")
            price = float(price_list[idx])
            product_total = quantity * price
            item = {
                "product_desc": product.name,
                "hsn_code": product.hsn_code,
                "mrp": product.mrp,
                "qty": quantity,
                "gst": 0,
                "disc": 0,
                "price": price,
                "amount": product_total
            }
            item_list.append(item)
            sub_total += product_total
        shop = Shop.objects.get(id=shop_id)
        context_data = {"shop_name": shop.name,
                        "shop_address": shop.address,
                        "item_details": item_list,
                        "sub_total": sub_total,
                        "total_in_words":
                            inf.number_to_words(sub_total).split("point")[0].capitalize()
                        }
        print(context_data)
        self.template_name="order/invoice.html"
        return self.render_to_response(context_data)

    def create_order(self, request):
        shop_id = request.POST.get("shop_id")
        product_list = request.POST.getlist("product_id")
        quantity_list = request.POST.getlist("quantity")
        # cost_price = request.POST.get("cp")
        price_list = request.POST.getlist("mrp")
        item_list = []
        sub_total = 0
        shop = Shop.objects.get(id=shop_id)
        order = Order.objects.create(customer=shop, order_no=shop.beat)

        for idx in range(len(product_list)):
            p_id = product_list[idx]
            product = Product.objects.get(id=p_id)
            quantity = float(quantity_list[idx])
            # cost_price = request.POST.get("cp")
            price = float(price_list[idx])
            product_total = quantity * price
            OrderItem.objects.create(order=order, product=product, quantity=quantity, mrp=price)
            stock = Stock.objects.get(product=product)
            stock.quantity-=quantity
            stock.save()
            sub_total += product_total
        Invoice.objects.create(order=order,sub_total =sub_total,outstanding_amount=sub_total)
