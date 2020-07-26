from decimal import Decimal
from myaccountant.baseviews import BaseAdminViews
from django.contrib import messages
from django.http.response import JsonResponse
from .models import Shop
from finance.models import PaymentLedger


class ShopAutoSuggest(BaseAdminViews):

    def get(self, request, *args, **kwargs):
        term = request.GET.get('term')
        ret_dict = {'data': []}
        products = list(Shop.objects.filter(name__icontains=term)
                        .values('id', 'name', 'beat'))
        ret_dict['data'].extend(products)
        ret_dict['success'] = True
        return JsonResponse(ret_dict)
