# Generated by Django 2.1 on 2020-07-16 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20200702_0045'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='gst',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='GST Number'),
        ),
    ]