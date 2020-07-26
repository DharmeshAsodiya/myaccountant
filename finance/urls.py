from django.contrib import admin
from django.urls import path
from .views import SupplierPaymentView, ShopPaymentView, PaymentLedgerSearchView

urlpatterns = [
    path('supplier-payment/', SupplierPaymentView.as_view()),
    path('shop-payment/', ShopPaymentView.as_view()),
    path('payment-ledger/search/', PaymentLedgerSearchView.as_view()),

]
