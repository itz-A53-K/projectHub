# Generated by Django 4.1.4 on 2023-02-21 08:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0026_remove_cart_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 2, 21, 13, 44, 30, 931110)),
        ),
    ]
