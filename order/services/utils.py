import json

from order.models import Order


def get_dated_order_details(start_date, end_date):
    details = []
    orders = Order.objects.filter(created_on__gte=start_date,
                                  created_on__lt=end_date).order_by("id")
    for o in orders:
        data = json.loads(o.invoice_details)
        tax = 0
        value = 0
        tax_5 = data["tax_details"].get("2.5", [0])[0]
        tax_12 = data["tax_details"].get("6.0", [0])[0]
        for key, val in data["tax_details"].items():
            tax += float(key)
            value += float(val[1])
        details.append((data['invoice_no'], data['invoice_date'], data.get('shop_gst', ''), value, tax_5, tax_5,
                        tax_12, tax_12, data['sub_total']))
    return details

# get_invoice_details("2020-07-01", "2020-08-01")
#
# get_invoice_details("2020-08-01", "2020-09-01")
#
# get_invoice_details("2020-09-01", "2020-10-01")