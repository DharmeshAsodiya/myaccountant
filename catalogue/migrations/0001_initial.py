# Generated by Django 2.1 on 2020-06-13 19:56

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=1000)),
                ('hsn_code', models.CharField(max_length=200)),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('mrp', models.DecimalField(decimal_places=2, max_digits=15)),
                ('created_by', models.ForeignKey(on_delete=False, related_name='product_created_on', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=False, related_name='product_updated_on', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('quantity', models.IntegerField(max_length=50)),
                ('created_by', models.ForeignKey(on_delete=False, related_name='stock_created_on', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=True, to='catalogue.Product')),
                ('updated_by', models.ForeignKey(on_delete=False, related_name='stock_updated_on', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StockInwardDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('quantity', models.IntegerField(max_length=50)),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('created_by', models.ForeignKey(on_delete=False, related_name='stockinwarddetails_created_on', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=True, to='catalogue.Product')),
                ('updated_by', models.ForeignKey(on_delete=False, related_name='stockinwarddetails_updated_on', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
