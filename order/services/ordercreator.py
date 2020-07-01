import datetime
from decimal import Decimal, ROUND_UP
import inflect

from client.models import Shop
from ..models import Order, OrderItem, Invoice
from catalogue.models import Product, Stock


class OrderCreator(object):

    def __init__(self, shop_id, product_list, quantity_list, price_list):
        self.order_total = Decimal(0)
        self.item_details = []
        self.order = None
        self.shop = None
        self.product_map = None
        self.tax_details = None
        self.tax_total = Decimal(0)
        self._build_order_details(shop_id, product_list, price_list, quantity_list)

    def _build_order_details(self, shop_id, product_list, price_list, quantity_list):
        self.shop = Shop.objects.get(id=shop_id)
        self.product_map = Product.objects.in_bulk(id_list=product_list)
        print(self.product_map)
        self.tax_details = {}
        for idx in range(len(product_list)):
            p_id = product_list[idx]
            product = self.product_map.get(int(p_id))
            quantity = Decimal(quantity_list[idx])
            price = Decimal(price_list[idx])
            tax_value = (product.tax_value / 100 * (quantity * price)).quantize(Decimal(".01"), rounding=ROUND_UP)
            product_total = quantity * price
            product_total = product_total.quantize(Decimal(".01"), rounding=ROUND_UP)
            tax = self.tax_details.get(product.tax_value)
            if tax:
                self.tax_details.update({product.tax_value/2: (tax + tax_value)/2})
            else:
                self.tax_details.update({product.tax_value/2: tax_value/2})
            item = {
                "product_id": product.id,
                "product_desc": product.name,
                "hsn_code": product.hsn_code,
                "mrp": product.mrp,
                "qty": quantity,
                "gst": product.tax_value,
                "disc": 0,
                "price": round(price, 2),
                "amount": product_total
            }
            self.item_details.append(item)
            self.order_total += product_total
            self.tax_total += tax_value

    def get_invoice_data(self):
        inf = inflect.engine()
        print(self.tax_details)
        final_total = self.order_total + sum(self.tax_details.values()) * 2
        return {"invoice_no": self.order.id if self.order else "NA",
                "invoice_date": datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%Y"),
                "shop_name": self.shop.name,
                "shop_address": self.shop.address,
                "item_details": self.item_details,
                "sub_total": self.order_total,
                "final_total": final_total,
                "tax_details": self.tax_details,
                "total_in_words":
                    inf.number_to_words(final_total).split("point")[0].capitalize()
                }

    def create_order(self):
        self.order = Order.objects.create(customer=self.shop, order_no=self.shop.beat)

        for item in self.item_details:
            product = Product.objects.get(id=item["product_id"])
            quantity = item["qty"]
            price = item["price"]
            OrderItem.objects.create(order=self.order, product=product,
                                     quantity=quantity, mrp=price)
            stock = Stock.objects.get(product=product)
            stock.quantity -= quantity
            stock.save()
        Invoice.objects.create(order=self.order, sub_total=self.order_total,
                               outstanding_amount=self.order_total)
