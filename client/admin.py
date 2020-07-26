from myaccountant.baseadmin import BaseAdmin
from django.contrib import admin
from .models import Shop


@admin.register(Shop)
class ShopAdmin(BaseAdmin):

    list_display = ('id', "name", "address", "beat", "contact_no", "gst", "outstanding_balance")
