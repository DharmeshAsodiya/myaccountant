import json

from django.views.generic.base import TemplateView
from decimal import Decimal
from myaccountant.baseviews import BaseAdminViews
from django.contrib import messages
from django.http.response import JsonResponse
from .models import Product, Stock, StockInwardDetails


class ProductInwardView(BaseAdminViews):

    template_name = "catalogue/productinward.html"

    # def dispatch(self, request, *args, **kwargs):
    #     return self.render_to_response(self.get_context_data())

    def post(self, request):
        product_name = request.POST.get("product")
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))
        cost_price = request.POST.get("cp")
        tax = request.POST.get("tax")
        mrp = request.POST.get("mrp")
        product = Product.objects.get(id=product_id)
        product.tax_value = tax
        stock, created = Stock.objects.get_or_create(product=product)
        if created:
            stock.created_by = request.user
            stock.updated_by = request.user
        stock.quantity += quantity
        stock.save()
        stock_value = Decimal(quantity) * Decimal(cost_price)
        StockInwardDetails.objects.create(product=product, quantity=quantity,
                                          cost_price=Decimal(cost_price), mrp=Decimal(mrp),
                                          stock_value=stock_value)
        messages.success(request, "Stock added, Final stock %s for %s" % (stock.quantity, stock.product))
        return self.render_to_response(self.get_context_data())


class ProductAutoSuggest(BaseAdminViews):

    def get(self, request, *args, **kwargs):
        term = request.GET.get('term')
        ret_dict = {'data': []}
        products = list(Product.objects.filter(name__icontains=term)
                        .values('id', 'name', "hsn_code", "mrp", "cost_price", "tax_value"))
        ret_dict['data'].extend(products)
        ret_dict['success'] = True
        return JsonResponse(ret_dict)

