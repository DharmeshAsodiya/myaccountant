from django.contrib import admin
from django.urls import path
from .views import ShopAutoSuggest

urlpatterns = [
    path('shop-autocomplete/', ShopAutoSuggest.as_view()),
]
