from django.contrib import admin
from django.urls import path
from .views import ProductInwardView, ProductAutoSuggest, SupplierAutoSuggest

urlpatterns = [
    path('product-inward/', ProductInwardView.as_view()),
    path('product-autocomplete/', ProductAutoSuggest.as_view()),
    path('supplier-autocomplete/', SupplierAutoSuggest.as_view()),
]
