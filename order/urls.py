from django.contrib import admin
from django.urls import path
from .views import OrderCreateView, InvoiceView
from .adminviews import DatedSalesReport

urlpatterns = [
    path('order-create/', OrderCreateView.as_view()),
    path('display-invoice/', InvoiceView.as_view()),
    path('sales-report/', DatedSalesReport.as_view())
]
