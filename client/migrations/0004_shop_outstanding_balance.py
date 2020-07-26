# Generated by Django 2.2.13 on 2020-07-18 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_shop_gst'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='outstanding_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
    ]
