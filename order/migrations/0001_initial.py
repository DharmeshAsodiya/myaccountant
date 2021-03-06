# Generated by Django 2.1 on 2020-06-14 14:04

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0001_initial'),
        # ('catalogue', '0002_auto_20200614_1934'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('paid_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('paid_at', models.DateTimeField(auto_now=True)),
                ('payment_mode', models.CharField(default='Cash', max_length=20)),
                ('created_by', models.ForeignKey(on_delete=False, related_name='creditnote_created_on', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('sub_total', models.DecimalField(decimal_places=2, max_digits=15)),
                ('outstanding_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('created_by', models.ForeignKey(on_delete=False, related_name='invoice_created_on', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('order_no', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(on_delete=False, related_name='order_created_on', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=True, to='client.Shop')),
                ('updated_by', models.ForeignKey(on_delete=False, related_name='order_updated_on', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('quantity', models.IntegerField(default=0)),
                ('mrp', models.DecimalField(decimal_places=2, max_digits=15)),
                ('created_by', models.ForeignKey(on_delete=False, related_name='orderitem_created_on', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(on_delete=True, to='order.Order')),
                ('product', models.ForeignKey(on_delete=False, to='catalogue.Product')),
                ('updated_by', models.ForeignKey(on_delete=False, related_name='orderitem_updated_on', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='invoice',
            name='order',
            field=models.ForeignKey(on_delete=True, to='order.Order'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='updated_by',
            field=models.ForeignKey(on_delete=False, related_name='invoice_updated_on', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='creditnote',
            name='invoice',
            field=models.ForeignKey(on_delete=True, to='order.Invoice'),
        ),
        migrations.AddField(
            model_name='creditnote',
            name='updated_by',
            field=models.ForeignKey(on_delete=False, related_name='creditnote_updated_on', to=settings.AUTH_USER_MODEL),
        ),
    ]
