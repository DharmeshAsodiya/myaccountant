import datetime
from decimal import Decimal, ROUND_UP
import inflect
import json


from client.models import Shop
from ..models import Order, OrderItem, Invoice
from catalogue.models import Product, Stock


def decimal_to_price(amount):
    return format(amount, ".2f")


class OrderCreator(object):

    def __init__(self, shop_id, product_list, quantity_list, price_list):
        self.order_total = Decimal(0)
        self.item_details = []
        self.order = None
        self.shop = None
        self.product_map = None
        self.tax_details = None
        self.tax_total = Decimal(0)
        self.total_payable = Decimal(0)
        self.invoice = None
        self._build_order_details(shop_id, product_list, price_list, quantity_list)

    def _build_order_details(self, shop_id, product_list, price_list, quantity_list):
        self.shop = Shop.objects.get(id=shop_id)
        self.product_map = Product.objects.in_bulk(id_list=product_list)
        self.tax_details = {}
        for idx in range(len(product_list)):
            p_id = product_list[idx]
            product = self.product_map.get(int(p_id))
            quantity = Decimal(quantity_list[idx])
            price = Decimal(price_list[idx])
            tax_value = (product.tax_value / 100 * (quantity * price)).quantize(Decimal(".01"), rounding=ROUND_UP)
            product_total = quantity * price
            product_total = product_total.quantize(Decimal(".01"), rounding=ROUND_UP)

            tax_key = float(product.tax_value / 2)
            tax = self.tax_details.get(tax_key, (0.0, 0.0))[1]
            tax_amount = tax_value
            if tax:

                tax_amount = Decimal(tax) + tax_value

            self.tax_details.update({tax_key: (decimal_to_price(tax_amount/2),
                                                    (decimal_to_price(tax_amount)))})
            item = {
                "product_id": product.id,
                "product_desc": product.name,
                "hsn_code": product.hsn_code,
                "mrp": decimal_to_price(product.mrp),
                "qty": int(quantity),
                "gst": float(product.tax_value),
                "disc": 0,
                "price": decimal_to_price(price),
                "amount": decimal_to_price(product_total)
            }
            self.item_details.append(item)
            self.order_total += product_total
            self.tax_total += tax_value

    def get_invoice_data(self):
        inf = inflect.engine()
        final_total = self.order_total + self.tax_total
        self.total_payable = Decimal(round(final_total, 0))
        total_in_words = inf.number_to_words(round(final_total, 0)).split("point")[0]
        invoice_details = {"invoice_no": self.order.id if self.order else "NA",
                           "invoice_date": datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%Y"),
                           "shop_name": self.shop.name,
                           "shop_address": self.shop.address,
                           "item_details": self.item_details,
                           "sub_total": decimal_to_price(self.order_total),
                           "final_total": decimal_to_price(final_total),
                           "roundup_total": decimal_to_price(round(final_total, 0)),
                           "roundup_diff": decimal_to_price(Decimal(round(final_total, 0)) - final_total),
                           "tax_details": self.tax_details,
                           "total_in_words": total_in_words
                          }

        return invoice_details

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
        details = self.get_invoice_data()
        self.invoice = Invoice.objects.create(order=self.order,
                                              sub_total=self.total_payable,
                                              outstanding_amount=self.total_payable,
                                              invoice_details=json.dumps(details))
        return self.invoice.id