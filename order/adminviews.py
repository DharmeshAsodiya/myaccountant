import csv

from django.http.response import HttpResponse

from myaccountant.baseviews import BaseAdminViews
from .services.utils import get_dated_order_details


class DatedSalesReport(BaseAdminViews):

    template_name = "order/reports/sales_report.html"

    def get_context_data(self, **kwargs):
        return {}

    def post(self, request):
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f"attachment; filename={from_date}-{to_date}.csv"

        headers = ("INV NO", "DATE", "GST NO", "TAXABLE VALUE", "SGST 2.5%", "CGST 2.5%", "SGST 6%", "CGST 6%", "TOTAL")
        order_details = get_dated_order_details(from_date, to_date)
        writer = csv.writer(response)
        writer.writerow(headers)
        writer.writerows(order_details)
        return response
