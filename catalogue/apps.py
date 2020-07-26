from django.apps import AppConfig


class CatalogueConfig(AppConfig):
    name = 'catalogue'

    operations = [
        ('product/product-inward/', '', 'Add Stock')
    ]