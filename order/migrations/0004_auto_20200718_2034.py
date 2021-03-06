# Generated by Django 2.2.13 on 2020-07-18 15:04

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20200716_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='invoice_details',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='outstanding_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AddField(
            model_name='order',
            name='sub_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.DeleteModel(
            name='CreditNote',
        ),
    ]
