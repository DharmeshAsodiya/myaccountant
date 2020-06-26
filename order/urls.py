from django.contrib import admin
from django.urls import path
from .views import OrderCreateView

urlpatterns = [
    path('order-create/', OrderCreateView.as_view()),
]