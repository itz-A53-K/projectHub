# Generated by Django 4.1.7 on 2023-03-24 07:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0037_alter_order_order_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 24, 13, 10, 22, 256586)),
        ),
    ]
