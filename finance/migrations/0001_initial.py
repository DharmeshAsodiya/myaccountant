# Generated by Django 2.2.13 on 2020-07-18 16:26

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
            name='PaymentLedger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('client_id', models.IntegerField()),
                ('client_type', models.PositiveSmallIntegerField()),
                ('paid_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('paid_at', models.DateTimeField(auto_now=True)),
                ('payment_mode', models.PositiveSmallIntegerField(default=0)),
                ('transaction_id', models.CharField(blank=True, max_length=200, null=True)),
                ('created_by', models.ForeignKey(on_delete=False, related_name='paymentledger_created_on', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=False, related_name='paymentledger_updated_on', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
